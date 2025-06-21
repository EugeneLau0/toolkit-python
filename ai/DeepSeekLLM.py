from langchain_core.language_models.llms import BaseLLM
from langchain_core.outputs import LLMResult
from typing import Optional, List, Dict, Any, Iterator
import requests


class DeepSeekLLM(BaseLLM):
    """封装DeepSeek LLM"""
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
