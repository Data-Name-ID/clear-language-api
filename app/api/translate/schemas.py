from pydantic import BaseModel


class TranslateRequest(BaseModel):
    text: str


class TranslationResult(BaseModel):
    translated_text: str


class TranslateResponse(BaseModel):
    translated_text: str
