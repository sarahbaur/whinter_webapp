from flask import Flask, request, render_template, jsonify
import os
import whisper
from pydub import AudioSegment
from pydub.silence import split_on_silence
import re

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB limit, for example


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/variage')
def variage():
    return render_template('variage.html')


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    print("Received transcription request")
    audio_file = request.files['audiofile']
    model_type = request.form['model_type']
    print("Processing file:", audio_file.filename, "with model:", model_type)

    filename = os.path.join('uploads', audio_file.filename)
    audio_file.save(filename)
    model = whisper.load_model(model_type)
    result = model.transcribe(filename)
    print("Transcription result:", result['text'])

    # Clean up the uploaded file after processing
    os.remove(filename)
    return jsonify({"transcription": result['text']})

@app.route('/transcribe_variage', methods=['POST'])
def transcribe_variage_audio():
    try:
        print("Received transcription request for variage")
        audio_file = request.files['audiofile']
        model_type = request.form['model_type']
        print("Processing file:", audio_file.filename, "with model:", model_type)

        filename = os.path.join('uploads', audio_file.filename)
        audio_file.save(filename)

        print("Loading model:", model_type)
        model = whisper.load_model(model_type)

        print(f"Reading file: {filename} via pydub")
        audio = AudioSegment.from_file(filename)

        print("Splitting on silence...")
        chunks = split_on_silence(audio, silence_thresh=-40, min_silence_len=1000)
        print(f"Number of chunks: {len(chunks)}")

        transcription = " ... ".join([transcribe_audio_segment(model, chunk) for chunk in chunks])
        transcription_clean = apply_transcription_rules(transcription)

        # Clean up the uploaded file after processing
        os.remove(filename)
        return jsonify({'transcription': transcription_clean})
    except Exception as e:
        print("Error in /transcribe_variage route:", e)
        # This sends a 500 plus the error message back to the client
        return jsonify({"error": str(e)}), 500


def transcribe_audio_segment(model, audio_segment: AudioSegment) -> str:
    temp_file = "temp_segment.wav"
    audio_segment.export(temp_file, format="wav")
    result = model.transcribe(temp_file)
    os.remove(temp_file)  # Clean up the temporary file
    return result['text']



def apply_transcription_rules(transcription: str) -> str:
    transcription = re.sub(r'(?<! )\.\.\.(?! )', ' ... ', transcription)
    transcription = re.sub(r'(\s*\.\.\.\s*)+', ' ... ', transcription)
    return transcription.strip()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 80)), debug=True)