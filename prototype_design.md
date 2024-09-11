# Prepared.ai Prototype Design

*Prepared.ai* is a multi-LLM based agent application that guides users in preparing for interviews or exams by creating personalized learning plans, generating coding questions, conducting mock interviews, and tracking progress. At its core, an LLM called AITutor dynamically writes Python code to call specialized tools like LearningPlanManager, CodingQuestionManager, and MemoryManager, providing an adaptive and personalized learning experience. The platform differentiates itself from generic chatbots by offering real-time orchestration, memory-driven progress tracking, adaptive learning paths, and detailed feedback after mock interviews, making it ideal for people looking to sharpen their skills for technical interviews and exams.


### **Core Design Components**

#### 1. **User Interface (UI)**
- **Goal Selection Panel:** Users will start by selecting their goal, e.g., "Practice coding for Company X interview" or "Prepare for a specific exam."
- **Learning Dashboard:** Display a summary of the user's progress, current learning plan, upcoming tasks, and achievements.
- **Interactive Mock Interview Panel:** Allows users to engage in real-time coding interviews, receiving feedback afterward.
- **Chat Box**: Provides a conversational interface for interacting with AITutor. Users can:
  - Provide answers, confirmations and prefrences.
  - Ask for help with questions.
  - Request explanations or hints for challenging topics.
  - Get personalized advice or adjustments to their learning plan in real-time.
****

## Chat with AITutor


#### 2. **AITutor Core**
- **Purpose:** AITutor is the central LLM-based agent that handles most of the user interaction. It generates Python code in real-time to interact with specialized modules (AI/non-AI tools) like LearningPlanManager, CodingQuestionManager, MemoryManager, etc.
  
- **Key Functions:**
    - **Goal Parsing:** Understands the user’s goals and requirements.
    - **Task Delegation:** Based on user input, AITutor dynamically generates Python code to invoke the right tool.
    - **Response Generation:** It processes feedback from submodules to generate accurate and personalized advice for the user.
    - **Error Handling:** It includes a built-in mechanism to handle failed tool interactions (fallback to prebuilt methods).
    - **Safety check:** AITutor will implement a real-time safety mechanism that checks user input for potentially harmful or malicious code. This function includes:
      -  Scans user input for suspicious patterns (e.g., unauthorized system commands, network access attempts, or file manipulations).
      - Runs any user-provided code in a secure, isolated environment to avoid system-wide effects.
  
- **Reason for Uniqueness:** AITutor’s ability to write and execute Python code dynamically, rather than simply generating text responses, allows it to orchestrate more complex workflows by delegating tasks to specialized modules.

#### 3. **Modules/Tools Integrated via AITutor**

   - **LearningPlanManager:**
     - **Functionality:** It builds a custom learning plan for each user, considering the goal, time constraints, and knowledge level.
     - **Tree Structure:** LearningPlanManager will use a tree structure to track subjects and subtopics with real-time progress updates, allowing users to drill down into specific areas.
     - **Progress Tracking:** Monitors learning status and updates the plan dynamically as users complete tasks or face difficulties.

   - **CodingQuestionManager:**
     - **Functionality:** Generates practice questions based on difficulty. Provides hints and grades responses.
     - **Grading:** Grades user answers and provides a final score with explanation.
     - **Potential improvements:** Avoid repeating questions, more personalization. Use question bank. Provide similar questions based on concept. Break down diffult problems into small chunks etc.

   - **MCQQuestionManager:**
     Similar to CodingQuestionManager but a only asks MCQ questions for faster assessment and objective grading.

   - **MockInterviewManager:**
     - **Functionality:** Simulates coding/design/behavioural interviews by posing coding and non coding problems and providing feedback on user solutions.
     - **AI-powered Evaluation:** Uses models to evaluate code submissions and provide structured feedback, mimicking a real-world interviewer.
     - **Simulate real interview:** Tracks time, provides hints and clears doubts similar to a real interviewer. Can be customized based on goal of user.

   - **MemoryManager:**
     - **Functionality:** Keeps track of the user’s preferences, learning gaps, strengths, and weaknesses. 
     - **Progress-Based Adjustments:** Allows the AITutor to offer tailored challenges, revisiting previous topics or introducing new ones based on historical data.
     - **Scope:** Keeping it simple (key val dictionary val <200 chars>) for the prototype as entire memory is printed as part of the prompt now. A complecated memory will make training difficult and increase prompt length. But scope should be increased in future to hold other datatypes and larger string values. We can also have LRU and RAG based memory for short term vs long term.
     
> TODO: Refinement and finalization of tools and their responsibilities will be done in final design.

For simplicity, all tool APIs should take input in primitive datatypes (int, str, float, array[primitive]) and produce primitive outputs. The benefits to this will be faster training of AI tutor as it does not need to know about the custom argment and return data types. 
#### 4. **Data Flow Architecture**

- **Step 1: Goal Definition:** Users input a goal (e.g., "Prepare for FAANG-level interviews"), and the AITutor processes this input.
- **Step 2: Learning Plan Generation:** AITutor calls the LearningPlanManager to create an individualized study roadmap. It may query user history from the MemoryManager to personalize the plan further. AITutor will push the user to lock the plan so progress can be tracked. Another option is to lock some plan initially and let the user modify it.
- **Step 3: Question Generation & Learning:** AITutor calls the CodingQuestionManager and MCQQuestionManager to serve coding problems or theory-based questions.
- **Step 4: Tracking & Adjustments:** User preference is continuously monitored by the MemoryManager and progress is evaluated by the LearningPlanManager, based on which the AITutor can do adjustments in future.
- **Step 5: Mock Interviews & Feedback:** The user engages in a mock interview where MockInterviewManager provides interactive feedback. The results get logged for further improvement.

---

### **Differentiation from Generic Chatbots:**

1. **True Multi-Agent Orchestration:**
   - Generic chatbots rely on a single LLM to handle all tasks, but *Prepared.ai* delegates responsibilities between specialized agents (LearningPlanManager, MemoryManager, CodingQuestionManager), enhancing both precision and functionality.

2. **Code-Driven Task Automation:**
   - AITutor’s ability to write code to call other services gives *Prepared.ai* a significant advantage in handling complex workflows that are impossible for traditional LLMs to manage on their own.

3. **Specialized for Interview and Exam Preparation:**
   - Unlike general-purpose chatbots, *Prepared.ai* is focused on a niche use case (interview and exam prep) with deep personalization, making it highly effective for users looking to improve their technical skills.

4. **AI-Powered Evaluation and Feedback Loops:**
   - Instead of only offering canned responses, *Prepared.ai* evaluates code, provides personalized feedback, and adjusts future tasks based on performance, providing a richer user experience.

This approach positions *Prepared.ai* as a unique learning and preparation tool, capable of far more sophisticated workflows than traditional conversational AI solutions. It leverages LLMs not just for chat but as agents orchestrating a comprehensive toolset designed to improve technical skills and track real progress.