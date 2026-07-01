import wave
from datetime import datetime
from pathlib import Path

import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
DURATION = 5
AUDIO_DIR = Path("audio_recordings")


def record_audio():
    print(f"Recording for {DURATION} seconds... speak now.")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()
    print("Recording finished.")
    return audio


def save_wav(audio, path: Path):
    AUDIO_DIR.mkdir(exist_ok=True)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())


def transcribe(path: Path):
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(path), beam_size=5)

    print(f"Detected language: {info.language} (confidence {info.language_probability:.2f})")
    full_text = ""
    for segment in segments:
        print(f"  [{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        full_text += segment.text
    return full_text.strip()


if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = AUDIO_DIR / f"recording_{timestamp}.wav"

    audio = record_audio()
    save_wav(audio, output_path)
    print(f"Saved to {output_path}")

    text = transcribe(output_path)
    print("\nFinal transcript:", text)