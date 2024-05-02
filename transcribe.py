import whisper
import argparse

def transcribe_audio(model, input_file: str) -> str:
    result = model.transcribe(input_file)
    return result['text']

def main(input_file, model_type):
    # Load the Whisper model directly using whisper.load_model()
    model = whisper.load_model(model_type)
    transcription = transcribe_audio(model, input_file)
    print(transcription)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio with Whisper.")
    parser.add_argument("input_file", type=str, help="Path to the input audio file.")
    parser.add_argument("model_type", type=str, choices=['tiny', 'base', 'small', 'medium', 'large'], help="Whisper model type to use for transcription.")
    args = parser.parse_args()

    main(args.input_file, args.model_type)
