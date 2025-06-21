from dotenv import load_dotenv
import os
from ai.DeepSeekLLM import DeepSeekLLM

load_dotenv()


llm = DeepSeekLLM(api_key=os.getenv("deepseek_api_key"))

# 直接调用
response = llm.invoke("你好！")
print(response)

# 在 LangChain Chain 中使用
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["question"],
    template="回答以下问题：{question}"
)
chain = LLMChain(llm=llm, prompt=prompt)
print(chain.invoke("你是谁？"))