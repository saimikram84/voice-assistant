from pathlib import Path

TTS_MODEL = "en_US-lessac-medium"
WHISPER_MODEL_SIZE = "base"
CLAUDE_MODEL = "claude-sonnet-5"

RECORDINGS_DIR = Path("audio_recordings")
OUTPUT_DIR = Path("audio_output")
RECORDING_PATH = RECORDINGS_DIR / "latest_input.wav"
OUTPUT_PATH = OUTPUT_DIR / "latest_output.wav"