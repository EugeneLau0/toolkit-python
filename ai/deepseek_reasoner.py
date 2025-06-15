from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("deepseek_api_key"), base_url="https://api.deepseek.com")

# 第一轮对话
messages = [{"role": "user", "content": "9.11 和 9.8, 哪个更大?"}]
# 指定模型
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)

reasoning_content = response.choices[0].message.reasoning_content
content = response.choices[0].message.content
print("round 1 reasoning_content: " + reasoning_content)
print("round 1 content:" + content)

# 第二轮对话：携带第一轮的content，以实现多轮对话
messages.append({'role': 'assistant', 'content': content})
messages.append({'role': 'user', 'content': "如果是序号比较，谁更大呢"})
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)

reasoning_content = response.choices[0].message.reasoning_content
content = response.choices[0].message.content
print("round 2 reasoning_content: " + reasoning_content)
print("round 2 content:" + content)
