from openai import OpenAI
class Orchestrator:
    def __init__(self):

        self.memory_manager = MemoryManager()
        self.user_profile_manager = UserProfileManager()
        self.user_skillset_manager = UserSkillsetManager()
        self.mcq_examiner = MCQExaminer(self.call_llm)
        self.coding_practice_tutor = CodingPracticeTutor(self.call_llm)
        self.chat_session = ChatSession()
        self.ai_teacher = AITeacher(self.call_llm, self.memory_manager, self.chat_session)
        self.client = OpenAI()

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
        response = self.ai_teacher.generate_response(user_input)
        self.chat_session.update_session('student', user_input)
        self.chat_session.update_session('aitutor', response)
        return response

class AITeacher:
    def __init__(self, call_llm, memory_manager, chat_session):
        self.call_llm = call_llm
        self.memory_manager = memory_manager
        self.chat_session = chat_session
        self.available_tools = {
            "MCQExaminer": "Provides MCQ questions based on user profile and skill level.",
            "CodingPracticeTutor": "Provides coding questions with boilerplate code."
        }

    def generate_response(self, input_text):
        # Construct prompt template with available tools and context
        prompt = f"""
        You are the AI Teacher. Available tools: {', '.join(self.available_tools.keys())}.
        Memory: {self.memory_manager.memory}.
        Chat history: {self.chat_session.get_last_n_messages(5)}.
        
        User Input: {input_text}

        Based on the above information, generate a suitable response. You can also say `call ToolName `
        """
        print(prompt)
        llm_response = self.call_llm(prompt)
        return llm_response

    def call_mcq_examiner(self, prompt):
        return self.call_llm(f"Generate an MCQ question on {prompt}")

    def call_coding_practice_tutor(self, prompt):
        return self.call_llm(f"Generate a coding question on {prompt}")

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
    
    def update_skill(self, skill, level):
        self.skills[skill] = level
    
    def get_skill(self, skill):
        return self.skills.get(skill, None)

class MCQExaminer:
    def __init__(self, call_llm):
        self.call_llm = call_llm
    
    def ask_question(self):
        return self.call_llm("Provide an MCQ question based on user profile and skill level.")

class CodingPracticeTutor:
    def __init__(self, call_llm):
        self.call_llm = call_llm
    
    def ask_question(self):
        return self.call_llm("Provide a coding question with boilerplate code.")

class ChatSession:
    def __init__(self):
        self.session_history = []
    
    def update_session(self, role, message):
        self.session_history.append(f"{role}: {message}")
    
    def get_last_n_messages(self, n):
        return self.session_history[-n:]

# # Example Usage
# orchestrator = Orchestrator()

# # Simulate a user interaction
# user_input = "I would like to practice some coding questions."
# response = orchestrator.process_user_input(user_input)
# print(response)
