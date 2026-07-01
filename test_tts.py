import subprocess
from datetime import datetime
from pathlib import Path

TEXT = "Hello, this is a test of the local text to speech pipeline."
MODEL = "en_US-lessac-medium"
AUDIO_DIR = Path("audio_output")


def synthesize(text: str, model: str, output_path: Path):
    AUDIO_DIR.mkdir(exist_ok=True)

    process = subprocess.run(
        ["uv", "run", "python", "-m", "piper", "--model", model, "--output_file", str(output_path)],
        input=text.encode("utf-8"),
        capture_output=True,
    )

    if process.returncode != 0:
        print("Piper failed:")
        print(process.stderr.decode("utf-8"))
    else:
        print(f"Saved synthesized speech to {output_path}")


if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = AUDIO_DIR / f"tts_{timestamp}.wav"

    synthesize(TEXT, MODEL, output_path)