```python
# Respond to the student acknowledging tat Generative AI is already added.
self.tools['Responder'].respond(f"I can confirm, Generative AI is already part of the learning program. \n\n {self.tools['LearningPlanManager'].get_plan_tree_markdown()}")
```