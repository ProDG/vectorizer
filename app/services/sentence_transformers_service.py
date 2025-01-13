import asyncio
import base64
from collections import defaultdict

from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.utils.common import StopWatch

transformers = defaultdict(dict)


def get_transformer(model_code, device_code):
    global transformers  # singleton

    if transformers.get(model_code, {}).get(device_code) is None:
        transformers[model_code][device_code] = SentenceTransformer(model_code, device=settings.device)

    return transformers[model_code][device_code]


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
