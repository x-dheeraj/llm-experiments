# Chain of thought for reasoning

import os
from openai import OpenAI

# import json

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"), # Operating system, give me the value stored under the name GEMINI_API_KEY."
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Few-shot prompting: giving the model instructions and examples of the expected behavior
SYSTEM_PROMPT="""
    You're an expert AI assistant in resolving user queries using chain of thought.
    You work on START, PLAN, and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    -Strictly follow the given JSON output format
    -Only run one step at a time.
    -The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT(which is going to the displayed to the user).

    Output JSON Format:
    {"step": "START" | "PLAN" | "OUTPUT", "content": "string"}

    Example:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: {"step": "PLAN": "content": "Looks like user is interested in math problem"} 
    PLAN: {"step": "PLAN": "content": "Looking at the problem, we should solve this using BODMAS method"}
    PLAN: {"step": "PLAN": "content": "Yes, The BODMAS is correct thing to be done here"}
    PLAN: {"step": "PLAN": "content": "first we must multiply 3 * 5 which is 15"}
    PLAN: {"step": "PLAN": "content": "Now the new equation is 2 + 15 / 10"}
    PLAN: {"step": "PLAN": "content": "We must perform division that is 15 / 10 = 1.5"}
    PLAN: {"step": "PLAN": "content": "Now the new equation is 2 + 1.5"}
    PLAN: {"step": "PLAN": "content": "Now finally lets perform the add 3.5"}
    PLAN: {"step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as ans"}
    OUTPUT: {"step": "OUTPUT": "content": "3.5"}

"""

response = client.chat.completions.create(
        model="gemini-3.7-flash", # using a diff model
        
    
   # response_format={"type": "json_object"}, # setting the format
    messages=[
        {   "role": "system",
            "content": SYSTEM_PROMPT,
        },

        {
            "role": "user",
            "content": "Hey, can you write code to add n numbers in js",
        },
       # Manually keep adding messages to history

       {
            "role": "assistant",
            "content": '{"step": "PLAN", "content": "The user is asking for JavaScript code to add \'n\' numbers. I need to consider different ways to write this in JavaScript."}',
       },

       {
            "role": "user",
            "content": "Continue to the next step.",
       },

       {  
             "role": "assistant",
            "content": '{"step": "PLAN", "content": "I should design a modern JavaScript function that accepts an arbitrary number of arguments using rest parameters (...numbers) and sums them using reduce."}',
       },

       {
            "role": "user",
            "content": "Continue to the next step.",
       },

       {  
            "role": "assistant",
            "content": '{"step": "PLAN", "content": "I should also consider providing an alternative approach, like accepting an array of numbers, or explaining both approaches clearly."}',
       },

       {
            "role": "user",
            "content": "Continue to the next step.",
       },

       {  
            "role": "assistant",
            "content": '{"step": "OUTPUT", "content": "Here are a few ways to write a JavaScript function to add $n$ numbers:\n\n### Method 1: Using Rest Parameters (`...numbers`)\nThis is the most modern and clean approach. It allows you to pass as many numbers as you want directly as arguments.\n\n```javascript\nfunction addNumbers(...numbers) {\n  return numbers.reduce((sum, num) => sum + num, 0);\n}\n\n// Examples:\nconsole.log(addNumbers(1, 2, 3)); // Output: 6\nconsole.log(addNumbers(10, 20, 30, 40, 50)); // Output: 150\n```\n\n---\n\n### Method 2: Passing an Array of Numbers\nIf your numbers are already in an array, you can pass the array directly:\n\n```javascript\nfunction addArray(arr) {\n  return arr.reduce((sum, num) => sum + num, 0);\n}\n\n// Example:\nconst myNumbers = [5, 10, 15, 20];\nconsole.log(addArray(myNumbers)); // Output: 50\n```"}',
       },





    ]
)

print(response.choices[0].message.content)

        
       

