```python
# Get a new MCQ question on Generative AI while waiting for the Concept Tutor's response.
question = self.tools['MCQExaminer'].get_question(
    subject="Generative AI",
    difficulty="medium"
)

# Respond with the new question.
self.tools['Responder'].respond(f"Here's another challenge for you: {question}")
```