import streamlit as st
import os
import time
from voice_processor import VoiceProcessor
from llm_handler import LLMHandler
from tts_handler import TTSHandler
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="Car Sales Voice Assistant", page_icon="🚗", layout="centered")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
    }
    .stChatFloatingInputContainer {
        padding-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm" not in st.session_state:
    st.session_state.llm = LLMHandler()

if "voice" not in st.session_state:
    st.session_state.voice = VoiceProcessor()

if "tts" not in st.session_state:
    st.session_state.tts = TTSHandler()

# Header
st.title("🚗 Car Sales Voice Assistant")
st.subheader("Your AI-powered car buying guide")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

# Voice Input Section
st.write("---")

if st.button("🎤 Start Speaking"):
    with st.spinner("Listening... (Speak now, I'll stop when you're finished)"):
        # 1. Capture and Transcribe
        user_text = st.session_state.voice.record_until_silence()
        
    if user_text.strip():
        # Display User Message
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.markdown(user_text)

        # 2. Assistant Response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # 2a. LLM Response - Generate full response first for simultaneous delivery
            with st.spinner("Thinking..."):
                full_response = ""
                # Stream the response from Gemini in the background
                response_stream = st.session_state.llm.get_response(user_text, stream=True)
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
            
            # 2b. TTS Response - Generate audio from full text
            with st.spinner("Preparing voice guide..."):
                audio_response = st.session_state.tts.text_to_speech_stream(full_response)
                audio_file = st.session_state.tts.save_audio(audio_response)
            
            # 2c. Play audio AND display text simultaneously
            autoplay_audio(audio_file)
            
            # Simulated streaming for visual effect while audio plays
            displayed_text = ""
            for char in full_response:
                displayed_text += char
                message_placeholder.markdown(displayed_text + "▌")
                # Adjust sleep time to roughly match speech speed (approx 15-20 chars per sec)
                time.sleep(0.02)
            
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    else:
        st.warning("No speech detected. Please try again.")

# Sidebar Options
with st.sidebar:
    st.title("Settings")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.llm.reset_chat()
        st.rerun()
    
    st.info("""
    ### How to use:
    1. Adjust duration if needed.
    2. Click 'Start Speaking'.
    3. Ask about any car or sales related query.
    4. The assistant will reply with text and voice.
    """)
