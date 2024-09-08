from openai import OpenAI

import re
import os
from typing import Any
import pickle
from datetime import datetime
from IPython.display import display, Markdown
from tool import Tool
import planner_tool
import memory_tool
import json 

def format_metadata_openapi(tool_name: str, metadata: str) -> str:
    # Indent each line of the metadata by 4 spaces
    indented_metadata = "\n".join("    " + line for line in metadata.splitlines())
    # Combine the tool name with the indented metadata
    return f"- '{tool_name}':\n\n{indented_metadata}"


class Orchestrator:
    def __init__(self, session_name ):
        self.session_name = session_name
        self.memory_manager = memory_tool.MemoryManager()
        self.user_profile_manager = UserProfileManager()
        self.user_skillset_manager = UserSkillsetManager()
        self.mcq_examiner = MCQExaminer(self._call_llm)
        self.coding_practice_tutor = CodingPracticeTutor(self._call_llm)
        self.concept_tutor = ConceptTutor(self._call_llm)
        self.client = OpenAI()
        self.chat_session = ChatSession()
        self.responder = Responder(chat_session = self.chat_session)
        self.learning_plan_manager = planner_tool.LearningPlanManager(self._call_llm)
        self.ai_student = AIStudent(self._call_llm)
        self.init_ai_teacher()

    def init_ai_teacher(self):
        self.tools = {
            "MemoryManager": self.memory_manager,
            "MCQExaminer": self.mcq_examiner,
            "CodingPracticeTutor": self.coding_practice_tutor,
            "ConceptTutor": self.concept_tutor,
            "Responder": self.responder,
            "LearningPlanManager": self.learning_plan_manager
        }
        

        self.ai_teacher = AITeacher(
            _call_llm=self._call_llm,
            chat_session = self.chat_session,
            tools= self.tools
        )

        # print(self.tools)
        # self.ai_teacher.tools['AITeacher'] = self.ai_teacher

    def _call_llm(self,  prompt, system_prompt="You are a helpful AI tutor.", model ="gpt-4o-mini" ):
        # Replace with actual call to an LLM API, e.g., OpenAI's GPT
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return completion.choices[0].message.content

    def process_user_input(self, user_input):
        # Calls the AI Teacher with the necessary context
        self.chat_session.update_session("student", user_input)
        self.ai_teacher.process()
        self.save_state(f'states/{self.session_name}.pkl')

    def save_state(self, filename):
        """ Save the state of the Orchestrator to a file. """
        state = {
            'memory_manager': self.memory_manager,  # Assuming these are serializable
            'user_profile_manager': self.user_profile_manager,
            'user_skillset_manager': self.user_skillset_manager,
            'chat_session': self.chat_session,
            'learning_plan':self.learning_plan_manager.root
        }
        with open(filename, 'wb') as file:
            pickle.dump(state, file)

    @staticmethod
    def load_session(session_name, root = 'states'):
        """ Load the state of the Orchestrator from a file. """
        with open(f'{root}/{session_name}.pkl', 'rb') as file:
            state = pickle.load(file)
        
        # Reconstruct instances that need to be reinitialized
        orc = Orchestrator(session_name)
        orc.memory_manager = state['memory_manager']
        orc.user_profile_manager = state['user_profile_manager']
        orc.user_skillset_manager = state['user_skillset_manager']
        orc.chat_session = state['chat_session']
        orc.responder = Responder(chat_session = orc.chat_session)
        orc.learning_plan_manager.root = state['learning_plan']
        orc.init_ai_teacher()

        return orc


class AITeacher(Tool):
    def __init__(self, _call_llm, chat_session, tools, log_file="training_data_log.jsonl"):
        self._call_llm = _call_llm
        self.tools = tools
        self.tools['AITeacher'] = self # keep yourself also as a tool.
        self.chat_session = chat_session
        self.log_file = log_file
        # Ensure the log file exists
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as file:
                file.write("")

    def _get_formatted_tool_info(self):
        tool_metadata = {tool_name:tool._get_tool_metadata() for tool_name, tool in self.tools.items()}
        return '\n\n'.join([format_metadata_openapi(tool_name, tool_metadata) for tool_name, tool_metadata in tool_metadata.items()])

    def _get_system_prompt(self):
        system_prompt = '''You are an AI Teacher guiding a student toward their goals. Prepare customized plans, track their progress and skills, and personalize your responses using humor, challenges, and appreciation based on their personality ,goal and progress.


        # Instructions:

        - Generate Only Python Code to call the appropriate tools only using self.tools['<toolname>'].method(args).
        - No New Methods/Classes: Only use provided tools/methods.
        - No tools except you will output anything to the user. So you are responsible to pass on the results of tool calls to the user.
        - Memory: Store short but important information in memory which might be needed later.
        - LearningPlan: Focus on locking a customized learning plan to track progress.
        - Confirmation: Confirm with user before changing anything.
        - Responder: User responder to respond to the user. Always respond with a question.
        - Code guidelines: Always end the python code with either a Responder or AITeacher tool call.
        '''

        return re.sub(r'^ {8}', '', system_prompt, flags=re.MULTILINE)

    def _indent_except_first(self, text, indent='    '):
        lines = text.split('\n')
        if len(lines) <= 1:
            return text
        # Keep the first line as is, and indent all other lines
        return lines[0] + '\n' + '\n'.join(indent + line for line in lines[1:])


    def _get_prompt(self, additional_info:dict = {}):
        # Construct prompt template with available tools and context
        prompt = f'''
        # Tools Available:
        {self._get_formatted_tool_info()}

        # Memory: 
        {self.tools['MemoryManager'].get_memory_snapshot()}

        # Additional Info: 
        {additional_info}

        # Learning Plan:
        {self.tools['LearningPlanManager'].get_plan_tree_markdown()} 
        
        # Current Time: {datetime.now()}

        # Conversation History (Last 10): 
        {'- '+ '\n\n- '.join([self._indent_except_first(text) for text in self.chat_session.get_last_n_messages(10)])+'\n'}

        # Plan code: 
        '''
        prompt = re.sub(r'^ {8}', '', prompt, flags=re.MULTILINE)
        return prompt

    def _save_training_data(self, prompt: str, code: str):
        '''Saves the generated prompt and code in JSONL format.'''
        # Create a dictionary with the prompt and code
        data_entry = {
            "prompt": prompt,
            "code": code,
            "timestamp": datetime.now().isoformat()
        }

        # Serialize the dictionary to a JSON string
        data_line = json.dumps(data_entry)

        # Append the JSON string to the log file
        with open(self.log_file, "a") as log_file:
            log_file.write(data_line + "\n")
    def process(self, additional_info: dict = None):
        '''
        Plans and executes the next steps using available tools and past conversation history.

        Args:
            additional_info (dict): Placeholder to pass information during recursive calls.
        '''
        system_prompt = self._get_system_prompt()
        prompt = self._get_prompt(additional_info)
        code = self._call_llm(prompt, system_prompt = system_prompt, model = "ft:gpt-4o-mini-2024-07-18:macro-mate::A54aVOOO")

        # Save the prompt and code
        self._save_training_data(system_prompt + prompt, code)

        try:
            self._execute_code(code)
        except Exception as e:
            # Retry n times later.
            self.tools["Responder"].respond(f"Sorry, I am facing internal error. Can you try again?\n{e}")

class Responder(Tool):
    def __init__(self, chat_session):
        self.chat_session = chat_session

    def respond(self, message:str):
        '''Respond to the user with markdown message'''
        self.chat_session.update_session("Tutor", message)
        display(Markdown(f"**PrepareAI:** {message}"))

from datetime import datetime, timedelta
from typing import Any, Dict, Tuple


class UserProfileManager(Tool):
    def __init__(self):
        self.profile = {}
    
    def update_profile(self, key, value):
        self.profile[key] = value
    
    def get_profile(self, key):
        return self.profile.get(key, None)

class UserSkillsetManager(Tool):
    def __init__(self):
        self.skills = {}
    
    def update_skill(self, skill:str, level:str):
        '''Update relevant skill and it's level to track progress and customize responses.'''
        self.skills[skill] = level
    
    def get_skills(self):
        '''Fetch all skills.'''
        return self.skills


class MCQExaminer(Tool):
    def __init__(self, _call_llm):
        self._call_llm = _call_llm
    
    def get_question(self, subject: str, difficulty: str) -> str:
        """
        Get an MCQ question based on the subject and difficulty level.
        """
        return self._call_llm(f"Provide an MCQ question on {subject} with {difficulty} difficulty.  Do not output answer.")

    def grade_answer(self, question: str, answer: str) -> str:
        """
        Provide feedback on the given answer for the specified question. 
        Includes correct answer and explanation if possible.
        """
        return self._call_llm(f'''Grade the following answer for the question '{question}'.
        User's Answer: {answer}. 
        
        Format:
        *Score* = <Based on the difficulty and answer, provide the score between [0,1] for each question. Score format is score/max_score>

        *Explanation* = <explanation of the score>

        *Correct answer* = <Correct answer to the question and diff with user's answer>
        ''')

    def provide_hint(self, question: str) -> str:
        """
        Provide a hint related to a specific MCQ question.
        """
        return self._call_llm(f"Provide a hint for the MCQ question: '{question}'. Include hint instructions to guide the user.")

class CodingPracticeTutor(Tool):
    def __init__(self, _call_llm):
        self._call_llm = _call_llm
    
    def get_question(self, topic: str, difficulty: str) -> str:
        """
        Get a coding question based on the topic and difficulty level.
        """
        return self._call_llm(f"Provide a coding question on {topic} with {difficulty} difficulty. Do not output answer.")

    def grade_answer(self, question: str, answer: str) -> str:
        """
        Provide feedback on the given answer for the specified question. 
        Includes correct answer and explanation if possible.
        """
        return self._call_llm(f'''Grade the following answer for the question '{question}'.
        User's Answer: {answer}. 
        
        Format:
        *Score* = <Based on the difficulty and answer, provide the score between[ 0,5]. Score format is score/max_score>

        *Explanation* = <explanation of the score>

        *Correct answer* = <Correct answer to the question and diff with user's answer>
        ''')

    def provide_hint(self, question: str) -> str:
        """
        Provide a hint related to a specific coding problem.
        """
        return self._call_llm(f"Provide a hint for the coding problem described by: '{question}'. Include hint instructions to guide the user.")


class ConceptTutor(Tool):
    def __init__(self, _call_llm):
        self._call_llm = _call_llm
    
    def get_concept(self, topic: str, context: str|None = None) -> str:
        """
        Return the concepts of a topic. Personalized based on context. Keep it concise but helpful. Adjust difficulty based on context.
        """
        return self._call_llm(f'''You are a friendly AI tutor who can explain concepts  personalized based on the concept. 
        Topic: '{topic}' 
        Context: {context}
        Explanation: ''')

    def clear_doubts(self,  doubt: str, context: str|None = None) -> str:
        """
        clear doubt based on the give context. 
        """
        return self._call_llm(f'''
        You are a friendly AI tutor who can clear doubts. Keep it concise but helpful. Adjust difficulty based on context.
        Context: {context}
        Doubt: {doubt}
        Clarification: ''')

class AIStudent(Tool):
    def __init__(self, _call_llm):
        self._call_llm = _call_llm
    
    def respond(self, messages:list[str], personality = None) -> str:
        """
        AI student model to generate training data.
        """
        return self._call_llm(f'''You are a student who stumbled upon a new AI application to prepare for coding interview.
        Respond to the ai bot's response. 
        {'personality = '+ personality if personality else ''}
        messages: {messages}
        Your response
        *student*: ''')

class ChatSession:
    def __init__(self):
        self.session_history = []
    
    def update_session(self, role, message):
        self.session_history.append(f"*{role}*: {message}")
    
    def get_last_n_messages(self, n) ->list[str]:
        return self.session_history[-n:]

# # Example Usage
# orchestrator = Orchestrator()

# # Simulate a user interaction
# user_input = "I would like to practice some coding questions."
# response = orchestrator.process_user_input(user_input)
# print(response)
