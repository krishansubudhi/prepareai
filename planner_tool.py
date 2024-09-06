from dataclasses import dataclass, field
from typing import List, Optional, Dict

from tool import Tool


@dataclass
class Progress:
    stats:dict = field(default_factory=dict)
    score: float = 0.0

    def get_category(self) -> str:
        """Calculate score based on correct answers and questions solved."""
        if self.score > 40:
            return 'Diamond'
        elif self.score > 20:
            return 'Gold'
        elif self.score > 10:
            return 'Silver'
        else:
            return 'Bronze'

    def update(self, score:float, stats:dict):
        """Update progress with new data and recalculate score."""
        self.score += score
        self.stats.update(stats)

    def __str__(self):
        """Return a concise string representation of the progress."""
        return (f"Score: {self.score:.2f}")

@dataclass
class PlanNode:
    subject_name: str
    importance: float = 1
    progress: Progress = field(default_factory=Progress)
    children: dict[str, 'PlanNode'] = field(default_factory=dict)
    parent: Optional['PlanNode'] = None

    def add_child(self, child: 'PlanNode'):
        """Adds a child node to the current node."""
        child.parent = self
        self.children[child.subject_name] = child
        

    def update_progress(self, score:float, stats:dict = {}):
        """Updates progress and propagates changes to the parent node."""
        self.progress.update(score, stats)
        if self.parent:
            self.parent.update_progress(self.progress.score * self.importance, stats)

    def print_tree(self, level=0):
        """Prints the tree structure in Markdown format."""
        markdown = ""
        indent = "  " * level  # Indentation for Markdown
        markdown += f"{indent}- **{self.subject_name}** (Importance: {self.importance}, Score: {self.progress.score})\n"
        for child in self.children.values():
            markdown += child.print_tree(level + 1)
        return markdown


class LearningPlanManager(Tool):
    root = None

    def __init__(self, _call_llm) -> None:
        self._call_llm = _call_llm
        self.subject_node_map = {}

    def suggest_learning_plan(self, goal: str, special_instruction:str)-> str:
        '''Returns a formatted learning plan based on the user's goal and special_instruction. This does not finalize or store the plan.'''
        # Generate a plan using the LLM
        plan_suggestion_prompt = f'''Create a new learning plan for a student with the goal: {goal}, special_instruction: {special_instruction}. 
        
        Instruction:

        Plan should be a tree of subjects and their importance. Maximum tree depth should be 2. 
        Maximum 10 total subjects.
        Importance ranges from 0.1 to 1.0.

        
        Learning plan:
        '''
        suggested_plan = self._call_llm(plan_suggestion_prompt)
        return suggested_plan


    def _find_node(self, subject_name: str, node: Optional[PlanNode] = None) -> Optional[PlanNode]:
        """Recursively searches for a node by subject name."""
        if node is None:
            node = self.root

        if node.subject_name == subject_name:
            return node

        for child in node.children.values():
            found = self._find_node(subject_name, child)
            if found:
                return found
        return None

    def _clear_existing_plan(self):
        self.root = None
        self.subject_node_map = {}
    
    def lock_new_plan(self, plan:str):
        """Locks the new plan"""
        prompt = f'''
            Write python code to create a new Plan. 

            Available methods:
                _create_new_plan( plan_name:str) -> None # Initializes the plan.
                add_subject(self, subject_name: str, importance: float, parent_subject: str|None = None) -> None # Adds a new subject to the plan under a specified parent node. parent_subject can be None to add subject to plan root.

            Plan description: {plan}

            Instructions:
            - Generate Only Python Code to call the appropriate tools only using self.method_name(args).
            - No New Methods/Classes: Only use provided tools/methods.
        '''
        code_to_execute = self._call_llm(prompt)
        self._execute_code(code_to_execute)

    def _create_new_plan(self, plan_name:str) -> None:
        self._clear_existing_plan()
        self.root = PlanNode(plan_name)
        return self.root

    def add_subject(self, subject_name: str, importance: float, parent_subject: str|None = None) -> None:
        """Adds a new subject to the plan under a specified parent node. parent_subject can be None to add subject to plan root."""
        if parent_subject:
            parent_node = self._find_node(parent_subject)
            if not parent_node:
                raise ValueError(f"Parent subject {parent_subject} not part of the plan")
        else:
            parent_node = self.root
        if subject_name in self.subject_node_map:
            raise ValueError("Subject already exists in the plan. Delete it first.")
        
        new_node = PlanNode(subject_name=subject_name, importance=importance)
        parent_node.add_child(new_node)
        self.subject_node_map[subject_name] = new_node
    
    def delete_subject(self, subject_name: str):
        """Adds a new subject to the plan under a specified parent node. Raises ValueError if subject is not part of the plan."""
        node = self._find_node(subject_name)
        if not node:
            raise ValueError(f"{subject_name} not part of plan.")
        else:
            del node.parent[subject_name]

    def update_progress(self, subject_name: str, score: float):
        """Updates the progress for a specific subject and propagates changes."""
        node = self._find_node(subject_name)
        if node:
            node.update_progress(score, stats = {})
        else:
            raise ValueError("Node not found.")

    def get_plan_tree_markdown(self, subject_name: str|None = None) -> str:
        """Returns learning plan in a readable markdown format. subject_name is optional."""
        node = self.root 
        if subject_name:
            node = self._find_node(subject_name=subject_name, node=self.root)
        if node is None:
            return "No plan locked yet."
        return node.print_tree()

    def get_progress(self, subject_name: str) -> str:
        """Retrieves concise progress information for a specific subject."""
        node = self._find_node(subject_name)
        if node:
            return str(node.progress)
        else:
            raise ValueError("Subject not found.")
    

    def _get_tool_metadata(self):
        excludes = ['get_progress', 'update_progress', 'get_plan', 'clear_existing_plan', 'add_subject','delete_subject','get_plan_tree_markdown'] if not self.root else []
        return super()._get_tool_metadata(excludes=excludes)

