from yandex_cloud_ml_sdk import AsyncYCloudML
from yandex_cloud_ml_sdk._types.message import TextMessage
from yandex_cloud_ml_sdk.auth import OAuthTokenAuth

from app.api.translate.schemas import TranslationResult
from app.core.llm import BaseLLMManager
from app.core.store import Store


class YandexCloudManager(BaseLLMManager):
    def __init__(self, store: Store) -> None:
        super().__init__(store)

        auth = OAuthTokenAuth(self.store.config.yc.oauth_token)
        sdk = AsyncYCloudML(
            folder_id=self.store.config.yc.folder_id,
            auth=auth,
        )
        self._system_prompt = TextMessage(
            role="system",
            text=self.store.config.mc.instruction,
        )

        self._model = sdk.models.completions(self.store.config.yc.model_name)
        self._model = self._model.configure(
            temperature=self.store.config.mc.temperature,
        )

    async def complete(self, text: str) -> TranslationResult:
        user_query = TextMessage(role="user", text=text)
        response = await self._model.run(
            messages=[self._system_prompt, user_query],
            timeout=self.store.config.mc.timeout,
        )
        return TranslationResult(translated_text=response.alternatives[0].text)
