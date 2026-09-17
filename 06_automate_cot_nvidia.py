

import os
from openai import OpenAI

import json


# Connect to NVIDIA API
client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"), # get NVIDIA API key from the environment
    base_url="https://integrate.api.nvidia.com/v1"
)


SYSTEM_PROMPT = """
You are an expert AI assistant that solves user queries step by step.

You work using START, PLAN, and OUTPUT.

Rules:
- Return exactly ONE JSON object.
- Return only JSON.
- Do not return markdown or any other text.
- The sequence is START -> PLAN -> OUTPUT.
- Return only one step per response.

Output format:
{"step": "START" | "PLAN" | "OUTPUT", "content": "string"}

Example:
{"step": "PLAN", "content": "Apply BODMAS to solve the expression."}
"""


print("\n\n\n")

# Automating the processs
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

user_query = input("👉")
message_history.append({"role": "user", "content": user_query})

while True:

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        temperature=0.2,
        max_tokens=1024,
        extra_body={
            "top_k": 1,
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        },
        messages=message_history
    )

    raw_result = response.choices[0].message.content

    message_history.append({
        "role": "assistant",
        "content": raw_result
    })

    parsed_result = json.loads(raw_result)

    if parsed_result["step"] == "START":
        print("🔥", parsed_result["content"])

    elif parsed_result["step"] == "PLAN":
        print("🧠", parsed_result["content"])

    elif parsed_result["step"] == "OUTPUT":
        print("🤖", parsed_result["content"])
        break

    message_history.append({
        "role": "user",
        "content": "Continue to the next step."
    })


print("\n\n\n")


# OUTPUT :
# 👉hey can you solve 2 + 3 / 10 * 2 * 4 * 3 / 20
# 🧠 The user wants me to solve the math problem: 2 + 3 / 10 * 2 * 4 * 3 / 20. I need to apply the order of operations (BODMAS/BIDMAS) which means I should handle multiplication and division from left to right before addition.
# 🧠 First, I'll handle the division and multiplication from left to right. The expression is 2 + 3 / 10 * 2 * 4 * 3 / 20. Let's break it down step by step.
# 🧠 First, compute 3 / 10 = 0.3. The expression becomes 2 + 0.3 * 2 * 4 * 3 / 20.
# 🧠 Next, compute 0.3 * 2 = 0.6. The expression becomes 2 + 0.6 * 4 * 3 / 20.
# 🧠 Compute 0.6 * 4 = 2.4. The expression becomes 2 + 2.4 * 3 / 20.
# 🧠 Compute 2.4 * 3 = 7.2. The expression becomes 2 + 7.2 / 20.
# 🧠 Compute 7.2 / 20 = 0.36. The expression becomes 2 + 0.36.
# 🧠 Compute 2 + 0.36 = 2.36. The final answer is 2.36.
# 🤖 2.36
