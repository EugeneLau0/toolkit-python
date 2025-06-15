from openai import OpenAI
# 从env文件中加载api_key
from dotenv import load_dotenv
import os
load_dotenv()
# print(os.getenv("deepseek_api_key"))
client = OpenAI(
    api_key=os.getenv("deepseek_api_key"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "who are you "},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(client.models.list())

print(response.choices[0].message.content)