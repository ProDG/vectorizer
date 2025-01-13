from io import BytesIO
from typing import Annotated

from PIL import Image
from fastapi import APIRouter, Path, Query, File, Depends

from app.api.dependencies.auth import token_required
from app.api.schemas.vectorize_schemas import VectorizeOutput, TextPayload
from app.core.config import settings
from app.services.sentence_transformers_service import vectorize_content
from app.core.defs import TransformerModel, VectorSerializationMode, CalculationDevice


vectorize_router = APIRouter()


@vectorize_router.post('/{transformer_code}/text/', response_model=VectorizeOutput, status_code=201)
async def vectorize_text(
    payload: TextPayload,
    transformer_code: Annotated[TransformerModel, Path()],
    mode: VectorSerializationMode = Query(VectorSerializationMode.plain),
    device: CalculationDevice = Query(settings.device),
    _=Depends(token_required),
):
    return await vectorize_content(
        model_code=transformer_code,
        device_code=device,
        mode=mode,
        payload=payload.src_text,
    )


@vectorize_router.post('/{transformer_code}/image/', response_model=VectorizeOutput, status_code=201)
async def vectorize_image(
    transformer_code: Annotated[TransformerModel, Path()],
    src_image: Annotated[bytes, File()],
    mode: VectorSerializationMode = Query(VectorSerializationMode.plain),
    device: CalculationDevice = Query(settings.device),
    _=Depends(token_required),
):
    return await vectorize_content(
        model_code=transformer_code,
        device_code=device,
        mode=mode,
        payload=Image.open(BytesIO(src_image)),
    )
