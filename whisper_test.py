import whisper

# Load Whisper Model
model = whisper.load_model("base")  # Use 'tiny' for faster test

# Transcribe from Local Audio File
result = model.transcribe("Perfect.mp3")  # Or test_audio.webm if you have that
print("Transcription Result:", result["text"])