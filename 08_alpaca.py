# Alpaca style prompting : useful for structuring instructions in a consistent, instruction-following format.



import os
from openai import OpenAI

import json


# Connect to NVIDIA API
client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"), # get NVIDIA API key from the environment
    base_url="https://integrate.api.nvidia.com/v1"
)


SYSTEM_PROMPT = """
### Instruction:
Translate the following sentence into Spanish.

### Input
{user_input}

### Response:
Hola, ¿cómo estás?
"""



user_query = input("👉")
message_history = SYSTEM_PROMPT.format(user_input = user_query)

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
        messages= [
            {
              "role": "user",
              "content": message_history,
            }
            ]
    )

    print("🤖", response.choices[0].message.content)

    break

    

  



# Output:


# 👉hello, how is the weather today?


# Hola, ¿cómo está el clima hoy?

# 👉i just listened to the news, the reported conveyed that it might rain in the evening   

# Acabo de escuchar las noticias, el informe dijo que podría llover por la tarde.
