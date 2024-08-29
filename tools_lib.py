from openai import OpenAI

import re
import pickle
import inspect
from datetime import datetime
from IPython.display import display, HTML, Image, Markdown

def get_tool_metadata(tool):
    """
    Extracts metadata from a tool instance, including function names, signatures, and docstrings.
    
    Args:
    - tool: The instance of the tool to inspect.

    Returns:
    - A dictionary mapping function names to tuples of their signatures and docstrings.
    """
    tool_metadata = {}
    

    # Iterate over all attributes of the tool
    for name in dir(tool):
        if name.startswith('_'):
            continue
        attr = getattr(tool, name, None)
        if callable(attr):
            try:
                # Inspect the method if it's callable
                signature = inspect.signature(attr)
                docstring = inspect.getdoc(attr)
                tool_metadata[name] = {
                    'signature': str(signature),
                    'docstring': docstring or ""
                }
            except Exception as e:
                print(f"Error processing method {name}: {e}")
    
    return tool_metadata


def format_metadata_openapi(tool_name: str, metadata: dict) -> str:
    """
    Formats the metadata for tools into a compact OpenAPI-like string.

    Args:
    - tool_name: The name of the tool.
    - metadata: Dictionary mapping function names to their metadata.

    Returns:
    - A formatted string representation of the metadata in OpenAPI format.
    """
    output = [f"{tool_name}:"]
    
    for name, info in metadata.items():
        output.append(f"  {name}:{info['signature']}  # {info['docstring']}")

    return "\n".join(output)

class Orchestrator:
    def __init__(self):

        self.memory_manager = MemoryManager()
        self.user_profile_manager = UserProfileManager()
        self.user_skillset_manager = UserSkillsetManager()
        self.mcq_examiner = MCQExaminer(self.call_llm)
        self.coding_practice_tutor = CodingPracticeTutor(self.call_llm)
        self.client = OpenAI()
        self.chat_session = ChatSession()
        self.responder = Responder(chat_session = self.chat_session)
        self.init_ai_teacher()

    def init_ai_teacher(self):
        self.tools = {
            "MemoryManager": self.memory_manager,
            "UserProfileManager": self.user_profile_manager,
            "UserSkillsetManager": self.user_skillset_manager,
            "MCQExaminer": self.mcq_examiner,
            "CodingPracticeTutor": self.coding_practice_tutor,
            "Responder": self.responder,
        }
        

        self.ai_teacher = AITeacher(
            call_llm=self.call_llm,
            chat_session = self.chat_session,
            tools= self.tools
        )

        self.ai_teacher.tools['AITeacher'] = self.ai_teacher

    def call_llm(self, prompt):
        # Replace with actual call to an LLM API, e.g., OpenAI's GPT
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful tutor."},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return completion.choices[0].message.content

    def process_user_input(self, user_input):
        # Calls the AI Teacher with the necessary context
        code_to_execute = self.ai_teacher.generate_code(user_input)
        self.chat_session.update_session("student", user_input)

        # Extract code from Markdown (assuming code is enclosed in triple backticks)
        code_pattern = re.compile(r'```(?:python)?\n(.*?)\n```', re.DOTALL)
        match = code_pattern.search(code_to_execute)
        
        if match:
            code = match.group(1)
            # Display the code (optional)
            display(Markdown(f"```python\n{code}\n```"))
            exec(code)  # Execute the extracted code
        else:
            print("No valid code block found.")
        
        self.save_state('states/current.pkl')

    def save_state(self, filename):
        """ Save the state of the Orchestrator to a file. """
        state = {
            'memory_manager': self.memory_manager,  # Assuming these are serializable
            'user_profile_manager': self.user_profile_manager,
            'user_skillset_manager': self.user_skillset_manager,
            'chat_session': self.chat_session,
        }
        with open(filename, 'wb') as file:
            pickle.dump(state, file)

    @staticmethod
    def load_state(filename):
        """ Load the state of the Orchestrator from a file. """
        with open(filename, 'rb') as file:
            state = pickle.load(file)
        
        # Reconstruct instances that need to be reinitialized
        orc = Orchestrator()
        orc.memory_manager = state['memory_manager']
        orc.user_profile_manager = state['user_profile_manager']
        orc.user_skillset_manager = state['user_skillset_manager']
        orc.chat_session = state['chat_session']
        orc.init_ai_teacher()

        return orc


class AITeacher:
    def __init__(self, call_llm, chat_session, tools):
        self.call_llm = call_llm
        self.tools = tools
        self.chat_session = chat_session
        # print('fetching tool metadata')
        self.tool_metadata = {tool:get_tool_metadata(self.tools[tool]) for tool in self.tools}
        self.formatted_tool_info = '\n'.join([format_metadata_openapi(tool, tool_metadata) for tool, tool_metadata in self.tool_metadata.items()])
                                             
    def generate_code(self, input_text:str, additional_info:dict = {}):
        # Construct prompt template with available tools and context
        prompt = f"""
        You are the AI Teacher. Available tools:

        {self.formatted_tool_info}.

        Memory: {self.tools['MemoryManager'].memory}
        Chat history: {self.chat_session.get_last_n_messages(5)}
        Additional Information: {additional_info}
        Current time: {datetime.now()}
        User Input: {input_text}

        Generate only Python code that to call the appropriate tools by calling `self.tools['toolname'].method(args)` and respond to the user.
        Do not write new methods or classes.
        Do not use tools/methods other than the ones available.
        Use responder to respond the user. Update memory if necessary to store relevant information. 
        """

        # display(Markdown(prompt))
        code = self.call_llm(prompt)
        return code  # This should return Python code to be executed by the Orchestrator

class Responder:
    def __init__(self, chat_session):
        self.chat_session = chat_session

    def respond(self, message):
        # Append message to the list of messages to be yielded by the generator
        self.chat_session.update_session("Tutor", message)
        display(Markdown(f"**PrepareAI:** {message}"))


class MemoryManager:
    def __init__(self):
        self.memory = {}
    
    def update_memory(self, key, value):
        self.memory[key] = value
    
    def get_memory(self, key):
        return self.memory.get(key, None)

class UserProfileManager:
    def __init__(self):
        self.profile = {}
    
    def update_profile(self, key, value):
        self.profile[key] = value
    
    def get_profile(self, key):
        return self.profile.get(key, None)

class UserSkillsetManager:
    def __init__(self):
        self.skills = {}
    
    def update_skill(self, skill:str, level:str):
        self.skills[skill] = level
    
    def get_skills(self):
        return self.skills

class MCQExaminer:
    def __init__(self, call_llm):
        self.call_llm = call_llm
    
    def get_question(self, subject: str, difficulty: str) -> str:
        """
        Get an MCQ question based on the subject and difficulty level.
        """
        return self.call_llm(f"Provide an MCQ question on {subject} with {difficulty} difficulty.")

    def grade_answer(self, question: str, answer: str) -> str:
        """
        Provide feedback on the given answer for the specified question. 
        Includes correct answer and explanation if possible.
        """
        return self.call_llm(f"Grade the following answer for the question '{question}': {answer}. Provide the correct answer and explanation if possible.")

    def provide_hint(self, question: str) -> str:
        """
        Provide a hint related to a specific MCQ question.
        """
        return self.call_llm(f"Provide a hint for the MCQ question: '{question}'. Include hint instructions to guide the user.")

class CodingPracticeTutor:
    def __init__(self, call_llm):
        self.call_llm = call_llm
    
    def get_question(self, topic: str, difficulty: str) -> str:
        """
        Get a coding question based on the topic and difficulty level.
        """
        return self.call_llm(f"Provide a coding question on {topic} with {difficulty} difficulty.")

    def grade_answer(self, code: str, solution: str) -> str:
        """
        Grade the given code, providing feedback, the correct solution, and hints if needed.
        """
        return self.call_llm(f"Grade the following code: {code}. Compare it with the solution: {solution}. Provide feedback on correctness, include the correct solution.")

    def provide_hint(self, question: str) -> str:
        """
        Provide a hint related to a specific coding problem.
        """
        return self.call_llm(f"Provide a hint for the coding problem described by: '{question}'. Include hint instructions to guide the user.")


class ChatSession:
    def __init__(self):
        self.session_history = []
    
    def update_session(self, role, message):
        self.session_history.append(f"{role}: {message}")
    
    def get_last_n_messages(self, n) ->list[str]:
        return self.session_history[-n:]

# # Example Usage
# orchestrator = Orchestrator()

# # Simulate a user interaction
# user_input = "I would like to practice some coding questions."
# response = orchestrator.process_user_input(user_input)
# print(response)
