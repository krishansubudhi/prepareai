```python
question = "Insert the number 20 at position 3 in the array [5, 6, 7, 8]"
answer = """```python
array = [5, 6, 7, 8]
array.insert(3, 20)
print(array)
```"""

# Grade the answer using the CodingPracticeTutor tool.
response = self.tools['CodingPracticeTutor'].grade_answer(
    question=question,
    answer=answer
)

# Respond to the student with the grading result.
self.tools['Responder'].respond(response)

```