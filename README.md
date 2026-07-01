# 🎙️ AI Voice Assistant

A fully local, privacy-first voice AI assistant built with speech-to-text, an LLM brain, and text-to-speech, wrapped in a real-time chat interface. Speak or type, get a spoken (or written) response back.

Built as a hands-on exploration of voice AI pipelines: how STT, LLM reasoning, and TTS chain together, and the real engineering tradeoffs (latency, cost, local vs. cloud) involved in making that chain feel natural.

---

## ✨ Features

- 🎤 **Voice or text input**: record your voice or just type, both work in the same chat box
- 🧠 **Conversational memory**: the assistant remembers earlier turns in the session
- 🔒 **Local-first pipeline**: speech-to-text and text-to-speech run entirely on your machine, with no per-minute API costs
- ⚡ **Fast, modern LLM brain** powered by Anthropic's Claude
- 💬 **Clean chat UI** built with Streamlit, with a pinned input box and auto-playing spoken replies
- 🧩 **Modular architecture**: STT, LLM, and TTS live in independent, swappable modules under `src/`

---

## 🏗️ Architecture

```mermaid
flowchart LR
    A[🎤 Voice or ⌨️ Text Input] --> B{Input Type?}
    B -->|Voice| C[faster-whisper<br/>Speech-to-Text]
    B -->|Text| E
    C --> E[Claude API<br/>LLM Reasoning]
    E --> F[Piper TTS<br/>Text-to-Speech]
    F --> G[🔊 Spoken Reply]
    E --> H[💬 Text Reply]
```

| Stage | Tool | Runs where | Cost |
|---|---|---|---|
| Speech-to-Text | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Local (CPU) | Free |
| LLM reasoning | [Claude API](https://www.anthropic.com) | Cloud | Paid (per token) |
| Text-to-Speech | [Piper](https://github.com/OHF-Voice/piper1-gpl) | Local (CPU) | Free |
| Interface | [Streamlit](https://streamlit.io) | Local | Free |

---

## 🛠️ Tech Stack

- **Language:** Python 3.14+
- **Package manager:** [`uv`](https://docs.astral.sh/uv/)
- **STT:** faster-whisper (local Whisper implementation)
- **LLM:** Anthropic Claude (`anthropic` SDK)
- **TTS:** Piper (local neural TTS)
- **UI:** Streamlit
- **Config:** python-dotenv

---

## 📁 Project Structure

```
voice-assistant/
├── app.py                  # Streamlit UI, orchestrates the pipeline
├── main.py                 # CLI version (terminal-based, for quick testing)
├── src/
│   ├── config.py           # Shared constants and file paths
│   ├── stt.py               # Speech-to-text logic (faster-whisper)
│   ├── llm.py               # LLM logic (Claude API)
│   └── tts.py               # Text-to-speech logic (Piper)
├── tests/                  # Unit tests for the src modules
├── audio_recordings/       # Saved voice input (gitignored)
├── audio_output/           # Generated speech output (gitignored)
├── .env                     # Your API key (gitignored, never commit this)
├── .env.example             # Template for required environment variables
├── .gitignore
└── pyproject.toml           # Managed by uv
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.14 or higher
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed
- An [Anthropic API key](https://console.anthropic.com/)
- A working microphone (for voice input)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/voice-assistant.git
cd voice-assistant
```

### 2. Set up the environment

```bash
uv venv
uv sync
```

### 3. Configure your API key

Copy the example file and add your key:

```bash
cp .env.example .env
```

Then edit `.env` and set:

```
ANTHROPIC_API_KEY=your-actual-key-here
```

### 4. Download the Piper voice model

```bash
uv run python -m piper.download_voices en_US-lessac-medium
```

### 5. Run the app

**Streamlit UI (recommended):**
```bash
uv run streamlit run app.py
```
Opens automatically at `http://localhost:8501`.

**CLI version (for quick testing):**
```bash
uv run python main.py
```

---

## 🎯 Usage

1. Open the app in your browser.
2. Either type a message in the chat box, or click the mic icon to record your voice.
3. Your speech is transcribed locally with faster-whisper.
4. Claude generates a response, with full memory of the conversation so far.
5. The response is spoken back to you via Piper, and also shown as text.

---

## ⚙️ Configuration

All tunable settings live in `src/config.py`:

| Variable | Default | Description |
|---|---|---|
| `WHISPER_MODEL_SIZE` | `"base"` | Whisper model size (`tiny`, `base`, `small`, `medium`, `large`). Bigger means more accurate but slower. |
| `TTS_MODEL` | `"en_US-lessac-medium"` | Piper voice model |
| `CLAUDE_MODEL` | `"claude-sonnet-4-6"` | Anthropic model used for reasoning |

---

## 🩹 Troubleshooting

**`piper-download: program not found`**
Piper's voice downloader is a Python module, not a standalone binary. Run it with:
```bash
uv run python -m piper.download_voices en_US-lessac-medium
```

**`AttributeError: 'ThinkingBlock' object has no attribute 'text'`**
Claude's response can include a reasoning block before the answer. Always filter by `block.type == "text"` rather than assuming `response.content[0]` is the answer. This is already handled in `src/llm.py`.

**Windows symlink warning from Hugging Face**
This is harmless. Windows blocks symlinks unless Developer Mode is enabled, so faster-whisper falls back to copying files instead. There's no functional impact.

---

## 🗺️ Roadmap

- [ ] Voice-activity detection (auto-stop recording on silence, instead of a fixed max duration)
- [ ] Streaming responses to reduce perceived latency
- [ ] Deploy to a cloud host for shareable demo links
- [ ] Multi-language support

## 👤 Author

Built by [Asam](https://github.com/saimikram84), AI/ML Engineer.

If you found this useful, consider giving the repo a ⭐.
