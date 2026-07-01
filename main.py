import os
import subprocess
import wave
from pathlib import Path

import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from anthropic import Anthropic

load_dotenv()

SAMPLE_RATE = 16000
TTS_MODEL = "en_US-lessac-medium"
EXIT_PHRASES = {"exit", "quit", "stop", "goodbye"}

RECORDINGS_DIR = Path("audio_recordings")
OUTPUT_DIR = Path("audio_output")
RECORDING_PATH = RECORDINGS_DIR / "latest_input.wav"
OUTPUT_PATH = OUTPUT_DIR / "latest_output.wav"

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")

conversation_history = []


def record_audio(max_seconds=15):
    input("Press Enter, then speak (recording stops automatically after a pause)...")
    print("Listening...")

    audio = sd.rec(int(max_seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()

    print("Done listening.")
    return audio


def save_wav(audio, path: Path):
    RECORDINGS_DIR.mkdir(exist_ok=True)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())


def transcribe(path: Path) -> str:
    segments, info = whisper_model.transcribe(str(path), beam_size=5)
    text = "".join(segment.text for segment in segments)
    return text.strip()


def ask_claude(prompt: str) -> str:
    conversation_history.append({"role": "user", "content": prompt})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=conversation_history,
    )

    reply_text = next(
        (block.text for block in response.content if block.type == "text"),
        ""
    )

    conversation_history.append({"role": "assistant", "content": reply_text})
    return reply_text


def synthesize(text: str, output_path: Path) -> bool:
    OUTPUT_DIR.mkdir(exist_ok=True)
    process = subprocess.run(
        ["uv", "run", "python", "-m", "piper", "--model", TTS_MODEL, "--output_file", str(output_path)],
        input=text.encode("utf-8"),
        capture_output=True,
    )
    if process.returncode != 0:
        print("Piper failed:")
        print(process.stderr.decode("utf-8"))
        return False
    return True


def play_audio(path: Path):
    data, samplerate = sf.read(str(path), dtype="float32")
    sd.play(data, samplerate)
    sd.wait()


def run_one_turn() -> bool:
    """Returns False when the conversation should end."""
    audio = record_audio()
    save_wav(audio, RECORDING_PATH)

    user_text = transcribe(RECORDING_PATH)
    print(f"You said: {user_text}")

    if not user_text:
        print("No speech detected, try again.")
        return True

    if user_text.lower().strip(".!? ") in EXIT_PHRASES:
        print("Ending conversation.")
        return False

    reply_text = ask_claude(user_text)
    print(f"Claude says: {reply_text}")

    if synthesize(reply_text, OUTPUT_PATH):
        play_audio(OUTPUT_PATH)

    return True


if __name__ == "__main__":
    print("Voice assistant ready. Say 'exit' or 'quit' anytime to stop.\n")
    try:
        while run_one_turn():
            print()  # blank line between turns for readability
    except KeyboardInterrupt:
        print("\nInterrupted, shutting down.")