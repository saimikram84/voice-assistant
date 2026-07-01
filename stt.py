from pathlib import Path
from faster_whisper import WhisperModel

from config import WHISPER_MODEL_SIZE


def load_whisper_model() -> WhisperModel:
    return WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")


def transcribe(model: WhisperModel, path: Path) -> str:
    segments, info = model.transcribe(str(path), beam_size=5)
    return "".join(segment.text for segment in segments).strip()