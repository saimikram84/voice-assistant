import subprocess
from pathlib import Path

from .config import TTS_MODEL, OUTPUT_DIR


def synthesize(text: str, output_path: Path) -> tuple[bool, str]:
    OUTPUT_DIR.mkdir(exist_ok=True)
    process = subprocess.run(
        ["uv", "run", "python", "-m", "piper", "--model", TTS_MODEL, "--output_file", str(output_path)],
        input=text.encode("utf-8"),
        capture_output=True,
    )
    if process.returncode != 0:
        return False, process.stderr.decode("utf-8")
    return True, ""