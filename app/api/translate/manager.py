from app.core.accessors import BaseAccessor


class TranslatedManager(BaseAccessor):
    async def translate(self, text: str) -> str:
        return await self.store.llm_manager.complete(text)
