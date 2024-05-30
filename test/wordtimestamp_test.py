import whisper

# Load the Whisper model
model = whisper.load_model("base")

# Path to your audio file
audio_path = "src/audio5.wav"

# Transcribe the audio file with word timestamps
result = model.transcribe(audio_path, word_timestamps=True)

# Extract the segments with word-level timestamps
segments = result["segments"]

# Write the transcription with word-level timestamps to a file
with open("transcription_with_word_timestamps.txt", "w") as f:
    for segment in segments:
        for word in segment["words"]:
            start = word["start"]
            end = word["end"]
            text = word["word"]  # Assuming the key is 'word'
            f.write(f"[{start:.2f} - {end:.2f}] {text}\n")
