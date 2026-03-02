from fastapi import APIRouter, HTTPException

from app.api.translate.schemas import TranslateRequest, TranslateResponse
from app.core.depends import StoreDep

router = APIRouter(prefix="/translate", tags=["Перевод на ясный язык"])


@router.post(
    "",
    summary="Запрос на перевод текста на ясный язык",
    response_description="Успешный ответ",
)
async def translate(store: StoreDep, data: TranslateRequest) -> TranslateResponse:
    try:
        result = await store.translate_manager.translate(text=data.text)
        return TranslateResponse(translated_text=result.translated_text)
    except Exception as exc:
        raise HTTPException(status=500, detail=str(exc)) from exc
