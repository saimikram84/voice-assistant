import streamlit as st
from dotenv import load_dotenv

from config import RECORDINGS_DIR, RECORDING_PATH, OUTPUT_PATH
from stt import load_whisper_model, transcribe
from llm import load_claude_client, ask_claude
from tts import synthesize

load_dotenv()

st.set_page_config(page_title="AI Voice Assistant", page_icon="🎙️")


@st.cache_resource
def get_whisper_model():
    return load_whisper_model()


@st.cache_resource
def get_claude_client():
    return load_claude_client()


whisper_model = get_whisper_model()
client = get_claude_client()

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

st.title("🎙️ AI Voice Assistant")
st.caption("faster-whisper (STT) → Claude (brain) → Piper (TTS), fully local except the LLM call.")

for message in st.session_state.conversation_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Type or record a message", accept_audio=True)

if prompt:
    if prompt.audio:
        RECORDINGS_DIR.mkdir(exist_ok=True)
        with open(RECORDING_PATH, "wb") as f:
            f.write(prompt.audio.getvalue())

        with st.spinner("Transcribing..."):
            user_text = transcribe(whisper_model, RECORDING_PATH)
    else:
        user_text = prompt.text

    if not user_text:
        st.warning("No speech or text detected, try again.")
    else:
        with st.chat_message("user"):
            st.write(user_text)

        with st.spinner("Thinking..."):
            reply_text = ask_claude(client, st.session_state.conversation_history, user_text)

        with st.chat_message("assistant"):
            st.write(reply_text)

        with st.spinner("Generating speech..."):
            success, error = synthesize(reply_text, OUTPUT_PATH)
            if success:
                st.audio(str(OUTPUT_PATH), autoplay=True)
            else:
                st.error(f"TTS failed: {error}")