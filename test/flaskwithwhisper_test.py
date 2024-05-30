from flask import Flask, jsonify
import whisper

app = Flask(__name__)


model = whisper.load_model("base")

@app.route("/transcribe", methods=["GET"])
def transcribe_audio():
    audio_path = "test/audio5.wav"
    result = model.transcribe(audio_path, word_timestamps=True)
    segments = result["segments"]

    # Create a string with transcription and timestamps
    transcription_with_timestamps = []
    for segment in segments:
        for word in segment["words"]:
            start = word["start"]
            end = word["end"]
            text = word["word"]
            transcription_with_timestamps.append(f"[{start:.2f} - {end:.2f}] {text}")

    # Join the list into a single string
    transcription_text = "\n".join(transcription_with_timestamps)

    # Save transcription to a file
    with open("flaskwithwhisper.txt", "w") as f:
        f.write(transcription_text)

    # Return transcription as JSON response
    return jsonify({"transcription": transcription_text})

if __name__ == "__main__":
    app.run(debug=True)
