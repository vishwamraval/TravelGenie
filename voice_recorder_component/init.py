import streamlit.components.v1 as components

voice_recorder = components.declare_component(
    "voice_recorder",
    url="http://localhost:3001"
)

def component():
    return voice_recorder()