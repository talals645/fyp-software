from flask import Flask, request, jsonify
import os
import whisper
import tempfile

app = Flask(__name__)

# Load the Whisper model globally so it doesn't load for each request
model = whisper.load_model("base")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    # Check if the request contains a file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        # Transcribe the audio file with word timestamps
        result = model.transcribe(temp_file_path, word_timestamps=True)
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

        # Optionally save transcription to a file
        with open("transcription_with_word_timestamps.txt", "w") as f:
            f.write(transcription_text)

        # Return transcription as JSON response
        return jsonify({"transcription": transcription_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        # Ensure the temporary file is deleted after processing
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    app.run(debug=True)
