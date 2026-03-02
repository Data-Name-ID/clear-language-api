from abc import ABC, abstractmethod

from app.api.translate.schemas import TranslationResult
from app.core.accessors import BaseAccessor
from app.core.store import Store


class BaseLLMManager(BaseAccessor, ABC):
    def __init__(self, store: Store) -> None:
        super().__init__(store)

    @abstractmethod
    async def complete(self, text: str) -> TranslationResult: ...
