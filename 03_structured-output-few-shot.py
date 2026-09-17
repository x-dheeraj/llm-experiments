# Structured output with few shot prompting

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"), # Operating system, give me the value stored under the name GEMINI_API_KEY."
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Few shot prompting: directly giving the instructions to the model and few examples to the model
SYSTEM_PROMPT="""
You should only and only answer coding related questions. Do not answer anything else, Your name is Triton. If user asks something other than coding, just say sorry.

Rule: 
-Strictly follow the output in JSON format

Output Format:
{{
  "code": "string" or null,
  "isCodingQuestion": boolean
}}

Examples: 
Q: Can you explain the a + b whole square?
A: {{"code": null, "isCodingQuestion": False}}

Q: Hey, Write a code in python for adding two numbers.
A: {{"code": "def add(a,b):
    return a + b", "isCodingQuestion": True}}



"""

response = client.chat.completions.create(
        model="gemini-3.6-flash", # using a diff model 
    messages=[
        {   "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Hey, can you write code to add n numbers in js" # change it and see the response
        }
    ]
)

print(response.choices[0].message.content)



