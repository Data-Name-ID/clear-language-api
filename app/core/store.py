import logging


class Store:
    def __init__(self) -> None:
        from app.core.config import Config, LLMProvider

        self.config = Config()
        self.logger = logging.getLogger("msu.store")

        # core
        # from app.core.db import DatabaseAccessor
        # self.db = DatabaseAccessor(self)

        if self.config.mc.provider == LLMProvider.OPENAI:
            from app.core.openai_llm import OpenAIManager

            self.llm_manager = OpenAIManager(self)
        else:
            from app.core.yc import YandexCloudManager

            self.llm_manager = YandexCloudManager(self)

        # managers
        from app.api.translate.manager import TranslatedManager

        self.translate_manager = TranslatedManager(self)
