import whisper
model = whisper.load_model("large-v2")
result = model.transcribe(audio = "audios/04. Hr Tag.mp3",
                          language = "hi",
                          task = "translate",
                          word_timestamps=False)

print(result)
with open ("output.json", "w") as f:
    json.dump(f, result)