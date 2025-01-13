from typing import List

from fastapi import UploadFile
from pydantic import BaseModel

from defs import TransformerModel, CalculationDevice


class TextPayload(BaseModel):
    src_text: str


class ImagePayload(BaseModel):
    src_image: UploadFile


class VectorizeOutput(BaseModel):
    vector: List[float] | str
    exec_time: float
    model: TransformerModel
    device: CalculationDevice
