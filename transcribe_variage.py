import os
import whisper
import re
from pydub import AudioSegment
from pydub.silence import split_on_silence
import argparse

def load_whisper_model(model_name: str):
    return whisper.load_model(model_name)

def transcribe_audio(model, audio_segment: AudioSegment) -> str:
    temp_file = "temp_segment.wav"
    audio_segment.export(temp_file, format="wav")
    result = model.transcribe(temp_file)
    os.remove(temp_file)  # Clean up the temporary file
    return result['text']

def apply_transcription_rules(transcription: str) -> str:
    transcription = re.sub(r'(?<! )\.\.\.(?! )', ' ... ', transcription)
    transcription = re.sub(r'(\s*\.\.\.\s*)+', ' ... ', transcription)
    return transcription.strip()

def main(filepath, model_type):
    model = load_whisper_model(model_type)
    audio = AudioSegment.from_file(filepath)
    chunks = split_on_silence(audio, silence_thresh=-40, min_silence_len=1000)
    transcription = " ... ".join([transcribe_audio(model, chunk) for chunk in chunks])
    transcription_clean = apply_transcription_rules(transcription)
    os.remove(filepath)  # Remove the uploaded file after processing
    return transcription_clean

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio with Whisper.")
    parser.add_argument("input_file", type=str, help="Path to the input audio file.")
    parser.add_argument("model_type", type=str, choices=['small'], help="Whisper model type to use for transcription.")
    args = parser.parse_args()

    main(args.input_file, args.model_type)