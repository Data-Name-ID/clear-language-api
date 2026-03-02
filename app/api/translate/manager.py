from app.api.translate.schemas import TranslationResult
from app.core.accessors import BaseAccessor


class TranslatedManager(BaseAccessor):
    async def translate(self, text: str) -> TranslationResult:
        return await self.store.llm_manager.complete(text)
