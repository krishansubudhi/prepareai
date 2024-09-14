import torch
import transformers
from torch import nn
torch.__version__
from transformers import AutoModelForCausalLM, AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")
# model = AutoModelForCausalLM.from_pretrained(
#     "meta-llama/Meta-Llama-3.1-8B-Instruct",
#     torch_dtype=torch.bfloat16,
#     device_map = 'auto'
# )
  
# input_text = "What is the meaning of life?"

# # Tokenize and move input to the appropriate device (MPS or CPU)
# inputs = tokenizer(input_text, return_tensors="pt").to('mps')

# print(inputs['input_ids'].device, inputs['input_ids'].dtype)

# with torch.no_grad():
#     outputs = model.generate(**inputs, max_new_tokens=10, num_beams=1,)
#     print(tokenizer.decode(outputs[0]))


model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)


messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]

print("Calling pipeline")
outputs = pipeline(
    messages,
    max_new_tokens=10,
)
print(outputs[0]["generated_text"][-1])  
