from flask import Flask, request, render_template, jsonify
import whisper

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    print("Received transcription request")
    audio_file = request.files['audiofile']
    model_type = request.form['model_type']
    print("Processing file:", audio_file.filename, "with model:", model_type)
    audio_file.save(audio_file.filename)
    model = whisper.load_model(model_type)
    result = model.transcribe(audio_file.filename)
    print("Transcription result:", result['text'])
    return jsonify({"transcription": result['text']})


if __name__ == '__main__':
    app.run(debug=True)
