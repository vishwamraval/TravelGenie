import whisper
import base64
import tempfile

model = whisper.load_model("base")

def transcribe_audio(base64_audio):
    audio_data = base64.b64decode(base64_audio)
    with tempfile.NamedTemporaryFile(suffix=".webm") as temp_audio_file:
        temp_audio_file.write(audio_data)
        temp_audio_file.flush()
        result = model.transcribe(temp_audio_file.name)
        return result["text"]