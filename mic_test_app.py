import streamlit as st
import streamlit.components.v1 as components
import base64

# Declare Component
voice_recorder = components.declare_component(
    "voice_recorder",
    url="http://localhost:3001"
)

st.title("🎙️ Mic Button Test")

audio_base64 = voice_recorder()

if audio_base64:
    st.success("Audio Recorded!")
    st.markdown(f"Base64 Length: {len(audio_base64)}")
    with open("recorded_audio.webm", "wb") as f:
        f.write(base64.b64decode(audio_base64))
    st.audio("recorded_audio.webm")