from utils.speech_to_text import transcribe_audio

audio_path = "audio/sample.wav"  # put any audio file here

text = transcribe_audio(audio_path)

print("TRANSCRIPT:")
print(text)
