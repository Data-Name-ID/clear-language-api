from openai import AsyncOpenAI

from app.core.llm import BaseLLMManager
from app.core.store import Store


class OpenAIManager(BaseLLMManager):
    def __init__(self, store: Store) -> None:
        super().__init__(store)

        self._client = AsyncOpenAI(
            api_key=self.store.config.openai.api_key,
            base_url=self.store.config.openai.base_url,
        )
        self._model_name = self.store.config.openai.model_name

    async def complete(self, text: str) -> str:
        response = await self._client.chat.completions.create(
            model=self._model_name,
            messages=[
                {"role": "system", "content": self.store.config.mc.instruction},
                {"role": "user", "content": text},
            ],
            temperature=self.store.config.mc.temperature,
            timeout=self.store.config.mc.timeout,
        )
        return response.choices[0].message.content
