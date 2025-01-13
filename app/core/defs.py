from enum import Enum


class CalculationDevice(str, Enum):
    mps = 'mps'         # Apple Silicon
    cuda = 'cuda'       # nVidia CUDA
    npu = 'npu'         # Mobile or IoT platforms NPU
    hpu = 'hpu'         # AWS Habana Gaudi (DL1 instances)
    cpu = 'cpu'         # CPU


class VectorSerializationMode(str, Enum):
    plain = 'plain'
    encoded_bytes = 'encoded_bytes'


class TransformerModel(str, Enum):
    clip_ViT_B_32 = 'clip-ViT-B-32'
    clip_ViT_B_32_ml = 'clip-ViT-B-32-multilingual-v1'
