# Automating the previous example Chain of thought for reasoning

import os
from openai import OpenAI

import json


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
    PLAN: {"step": "PLAN", "content": "Looks like user is interested in math problem"} 
    PLAN: {"step": "PLAN", "content": "Looking at the problem, we should solve this using BODMAS method"}
    PLAN: {"step": "PLAN", "content": "Yes, The BODMAS is correct thing to be done here"}
    PLAN: {"step": "PLAN", "content": "first we must multiply 3 * 5 which is 15"}
    PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 15 / 10"}
    PLAN: {"step": "PLAN", "content": "We must perform division that is 15 / 10 = 1.5"}
    PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 1.5"}
    PLAN: {"step": "PLAN", "content": "Now finally lets perform the add 3.5"}
    PLAN: {"step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as ans"}
    OUTPUT: {"step": "OUTPUT", "content": "3.5"}

"""
print("\n\n\n")

# Automating the processs
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

user_query = input("👉")
message_history.append({"role": "user", "content": user_query})

while True:  # here we are creating an infinite loop
    response = client.chat.completions.create(
      model="gemini-3.8-flash",
    #   response_format = {"type": "json_object"},
        messages = message_history
    )


    raw_result = response.choices[0].message.content

    # save the models response to history
    message_history.append({"role": "assistant", "content": raw_result})

    
    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
        

    elif parsed_result.get("step") == "PLAN":
            print("🧠", parsed_result.get("content"))
            

    elif parsed_result.get("step") == "OUTPUT":
                print("🤖", parsed_result.get("content"))
                break

    # asking the model to continue unless OUTPUT was reached
    if parsed_result.get("step") != "OUTPUT":
        message_history.append({"role": "user", "content": "Continue to the next step."})


print("\n\n\n")


# OUTPUT :

# 👉hey can you solve 3 + 5 * 2 / 10
# 🧠 The user wants to solve the arithmetic expression: 3 + 5 * 2 / 10. I should apply BODMAS/PEMDAS rule.
# 🧠 According to order of operations (PEMDAS/BODMAS), multiplication and division take precedence over addition, processed from left to right. First, calculate 5 * 2 = 10.
# 🧠 Now the expression becomes 3 + 10 / 10. Next, evaluate the division operation: 10 / 10 = 1.
# 🧠 Now the expression is 3 + 1. Finally, perform the addition: 3 + 1 = 4.
# 🤖 The result of 3 + 5 * 2 / 10 is 4.