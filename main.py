import asyncio
import base64
from collections import defaultdict
from io import BytesIO
from typing import Annotated

from PIL import Image
from fastapi import FastAPI, Path, Query, File, UploadFile
from pydantic_settings import BaseSettings, SettingsConfigDict
from sentence_transformers import SentenceTransformer

from schemas import TextPayload, ImagePayload, VectorizeOutput
from defs import TransformerModel, VectorSerializationMode, CalculationDevice
from utils import StopWatch


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    device: CalculationDevice = CalculationDevice.cpu


settings = AppSettings()


transformers = defaultdict(dict)

def get_transformer(model_code, device_code):
    global transformers  # singleton

    if transformers.get(model_code, {}).get(device_code) is None:
        transformers[model_code][device_code] = SentenceTransformer(model_code, device=settings.device)

    return transformers[model_code][device_code]


app = FastAPI()


async def vectorize_content(*, model_code, device_code, payload, mode):
    with StopWatch() as sw:
        transformer = get_transformer(model_code, device_code)
        vector_serializer = {
            'plain': lambda v: v.tolist(),
            'encoded_bytes': lambda v: base64.b64encode(v.tobytes()).decode('ascii')
        }[mode]

        encoded_vector = await asyncio.to_thread(transformer.encode, payload, show_progress_bar=False)
        vector = vector_serializer(encoded_vector)

    return {
        'vector': vector,
        'exec_time': sw.elapsed_time,
        'model': model_code,
        'device': device_code,
    }

@app.post('/api/vectorize/{transformer_code}/text/', response_model=VectorizeOutput, status_code=201)
async def vectorize_text(
    payload: TextPayload,
    transformer_code: Annotated[TransformerModel, Path()],
    mode: VectorSerializationMode = Query(VectorSerializationMode.plain),
    device: CalculationDevice = Query(settings.device),
):
    return await vectorize_content(
        model_code=transformer_code,
        device_code=device,
        mode=mode,
        payload=payload.src_text,
    )


@app.post('/api/vectorize/{transformer_code}/image/', response_model=VectorizeOutput, status_code=201)
async def vectorize_image(
    transformer_code: Annotated[TransformerModel, Path()],
    src_image: Annotated[bytes, File()],
    mode: VectorSerializationMode = Query(VectorSerializationMode.plain),
    device: CalculationDevice = Query(settings.device),
):
    return await vectorize_content(
        model_code=transformer_code,
        device_code=device,
        mode=mode,
        payload=Image.open(BytesIO(src_image)),
    )