import whisper

# Load the Whisper model
model = whisper.load_model("base")

# Path to your audio file
audio_path = "src/audio5.wav"

# Transcribe the audio file with word timestamps
result = model.transcribe(audio_path, word_timestamps=True)

# Extract the segments with timestamps
segments = result["segments"]

# Write the transcription with timestamps to a file
with open("transcription_with_timestamps.txt", "w") as f:
    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        f.write(f"[{start:.2f} - {end:.2f}] {text}\n")
