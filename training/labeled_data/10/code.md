```python
question = """### Problem: Longest Substring Without Repeating Characters

Given a string, find the length of the longest substring without repeating characters.

#### Example

**Input:**
```
s = "abcabcbb"
```
**Output:**
```
3
```
**Explanation:**
The answer is "abc", with the length of 3.

**Input:**
```
s = "bbbbb"
```
**Output:**
```
1
```
**Explanation:**
The answer is "b", with the length of 1.

**Input:**
```
s = "pwwkew"
```
**Output:**
```
3
```
**Explanation:**
The answer is "wke", with the length of 3.
Note that the answer must be a substring, "pwke" is a subsequence and not a substring.

#### Constraints
- `0 <= s.length <= 5 * 10^4`
- `s` consists of English letters, digits, symbols, and spaces.

#### Function Signature
```python
def length_of_longest_substring(s: str) -> int:
```

#### Notes
- You can solve this using sliding window technique or hash maps.
- Focus on optimizing the solution to handle large input sizes efficiently.
"""

answer = """def length_of_longest_substring(s: str) -> int:
    longest_substr_len = 0
    current_substr_len = 0
    current_substr_chars = set()
    for c in s:
if c in current_substr_chars:
    continue
else:
    current_substr_len += 1
    longest_substr_len = max(longest_substr_len, current_substr_len)
    current_substr_chars.add(c)
    return longest_substr_len
"""

grader_response = self.tools['CodingPracticeTutor'].grade_answer(question = question, answer = answer)

self.tools['Responder'].respond(grader_response)

```