# 正确的新版导入（避免弃用警告）
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import os
from langchain_core.language_models.llms import BaseLLM
from langchain_core.outputs import LLMResult
from typing import Optional, List, Dict, Any, Iterator
import requests

load_dotenv()


class DeepSeekLLM(BaseLLM):
    api_key: str  # DeepSeek API Key
    model: str = "deepseek-chat"  # 默认模型
    temperature: float = 0.7  # 温度参数
    base_url: str = "https://api.deepseek.com/v1"  # DeepSeek API 地址

    def _generate(
            self,
            prompts: List[str],
            stop: Optional[List[str]] = None,
            run_manager: Optional[Any] = None,
            **kwargs: Any,
    ) -> LLMResult:
        """实现必须的抽象方法"""
        responses = []
        for prompt in prompts:
            response = self._call(prompt, stop=stop, **kwargs)
            responses.append(response)
        return LLMResult(generations=[[{"text": r}] for r in responses])

    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            **kwargs: Any,
    ) -> str:
        """调用DeepSeek API"""
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            **kwargs
        }
        if stop:
            data["stop"] = stop

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    @property
    def _llm_type(self) -> str:
        return "deepseek"


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