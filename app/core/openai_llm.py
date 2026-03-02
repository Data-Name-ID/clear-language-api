from openai import AsyncOpenAI

from app.api.translate.schemas import TranslationResult
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

    async def complete(self, text: str) -> TranslationResult:
        response = await self._client.responses.parse(
            model=self._model_name,
            instructions=self.store.config.mc.instruction,
            input=text,
            text_format=TranslationResult,
            temperature=self.store.config.mc.temperature,
            timeout=self.store.config.mc.timeout,
        )
        return response.output_parsed
