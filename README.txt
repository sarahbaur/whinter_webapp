# WHINTER - A Whisper Audio Transcription Application

This repository provides a Flask-based web application and command-line scripts to transcribe audio files using OpenAI's [Whisper](https://github.com/openai/whisper) automatic speech recognition (ASR) model.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Flask Application](#running-the-flask-application)
  - [Using the Command-Line Scripts](#using-the-command-line-scripts)
- [Endpoints](#endpoints)
- [Possible Customizations](#possible-customizations)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project demonstrates how to use Whisper to transcribe audio files via a web interface or via command-line utilities. The repository includes:

Root Directory:
- **app.py**: A Flask application that exposes two endpoints for transcription (`/transcribe` and `/transcribe_variage`).
- **transcribe.py**: A command-line script to transcribe a single audio file using one of Whisper's model variants (`tiny`, `base`, `small`).
- **transcribe_variage.py**: A command-line script that splits an audio file based on silence, transcribes each chunk using Whisper, then applies some text formatting rules.

Static Directory:
- css directory: Contains CSS files for styling the web interface.
- js directory: Contains JavaScript files for client-side functionality.
- imgs directory: Contains images used in the web interface.

Templates Directory:
- **base.html**: The main HTML template for the web interface, allowing users to upload an audio file and select a model for transcription.
- **variage.html**: A template for chunked transcription, where the audio is split on silence.

Uploads Directory:
- Temporary storage for uploaded audio files.

---

## Features

1. **Web Application**
   - Upload an audio file to be transcribed by Whisper.
   - Choose a model size (`tiny`, `base`, `small`).
   - Handle both basic transcription and more advanced "variage" transcription that splits on silence.

2. **Command-Line Utilities**
   - Simple script (`transcribe.py`) for direct file transcription.
   - Advanced script (`transcribe_variage.py`) that splits on silence, transcribes each chunk, and combines results.

3. **Automatic Cleanup**
   - Temporary files are removed after processing to save disk space.

4. **Customizable Functionalities**
---

## Requirements

- Python 3.7+
- [Whisper](https://github.com/openai/whisper)
- [Flask](https://pypi.org/project/Flask/)
- [pydub](https://pypi.org/project/pydub/)
- [ffmpeg](https://ffmpeg.org/) (required by pydub)

### Python Packages

- `openai-whisper`
- `Flask`
- `pydub`

You can install these via pip:

```bash
pip install openai-whisper Flask pydub
```

**Note**: If you have trouble installing `openai-whisper`, it may require additional dependencies such as PyTorch. Refer to the [Whisper repository](https://github.com/openai/whisper) for more details.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/whisper-audio-transcription.git
   cd whisper-audio-transcription
   ```

2. **Set Up a Virtual Environment (Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies:**

   ```bash
   pip install --upgrade pip
   pip install openai-whisper Flask pydub
   ```

4. **Install FFmpeg (if not already installed):**
   - On macOS using Homebrew: `brew install ffmpeg`
   - On Linux (Debian/Ubuntu): `sudo apt-get update && sudo apt-get install ffmpeg`
   - On Windows, download from the [FFmpeg website](https://ffmpeg.org/download.html) or use a package manager such as [chocolatey](https://chocolatey.org/) with `choco install ffmpeg`.

---

## Usage

### Running the Flask Application

1. **Create an `uploads` directory** (if it doesn't exist) where the audio files will be stored temporarily:

   ```bash
   mkdir uploads
   ```

2. **Run the application:**

   ```bash
   python app.py
   ```

3. **Access the web interface:**
   Visit [http://localhost:5000](http://localhost:5000) in your browser.

4. **Transcription**
   - **`/transcribe`** endpoint for single-shot transcription.
   - **`/transcribe_variage`** endpoint for chunked transcription (splitting audio on silence).

### Using the Command-Line Scripts

#### `transcribe.py`

Transcribes a single audio file using the selected Whisper model.

```bash
python transcribe.py <input_file> <model_type>
```

- **`<input_file>`**: Path to the input audio file (e.g., `path/to/audio.mp3`).
- **`<model_type>`**: Whisper model type (one of `tiny`, `base`, or `small`).

Example:

```bash
python transcribe.py sample_audio.mp3 small
```

#### `transcribe_variage.py`

Splits the audio file on silence, transcribes each chunk, and applies custom text rules (e.g., converting `...` to spaced segments).

```bash
python transcribe_variage.py <input_file> <model_type>
```

- **`<input_file>`**: Path to the input audio file.
- **`<model_type>`**: Currently set to `small` in the argparse choices.

Example:

```bash
python transcribe_variage.py sample_audio.wav small
```

**Note**: This script deletes the input file (`sample_audio.wav`) after processing, so ensure you have a backup if needed.

---

## Endpoints

1. **GET `/`**
   - Renders `base.html`, which allows you to upload a file and select a model to transcribe.

2. **GET `/variage`**
   - Renders `variage.html` for chunked transcription (splitting on silence).

3. **POST `/transcribe`**
   - **Request**
     - `audiofile`: The uploaded audio file.
     - `model_type`: The Whisper model type (`tiny`, `base`, `small`).
   - **Response**: JSON containing `"transcription"`.

4. **POST `/transcribe_variage`**
   - **Request**
     - `audiofile`: The uploaded audio file.
     - `model_type`: The Whisper model type (`tiny`, `base`, `small`).
   - **Response**: JSON containing `"transcription"` of concatenated chunks.

---

## Possible Customizations

Here are some ways to adapt or extend this application:

1. **Adding a Different Whisper Model**
   - Modify the `choices` in the argparse sections (`transcribe.py` and `transcribe_variage.py`) or the dropdown in the HTML templates to include other model options (e.g., `medium`, `large`).
   - Update the `load_model` calls (`whisper.load_model(model_type)`) accordingly.

2. **Changing the Silence Threshold or Minimum Silence Length**
   - In `transcribe_variage.py` and `app.py` (for the `/transcribe_variage` endpoint), change the arguments in `split_on_silence` (e.g., `silence_thresh=-50` or `min_silence_len=500`) to suit your specific audio conditions.

3. **Adjusting the Text Cleaning Rules**
   - In `apply_transcription_rules`, you can add or remove regular expressions. For example, if you want to remove repeated punctuation or handle different spacing rules, update or replace the existing regex patterns.

4. **Preserving the Original Audio File**
   - Currently, both `transcribe_variage.py` and the Flask route remove the uploaded file after processing. If you need to keep the file,  remove or comment out the `os.remove(filepath)` calls.

---

## Project Structure

```
.
├── app.py                  # Flask application
├── transcribe.py           # Command-line script for single-shot
├── transcribe_variage.py   # Command-line script for chunked transcription
├── static                 # Static files (CSS, JS, images)
│   ├── css
│   ├── js
│   └── imgs
├── templates              # HTML templates
│   ├── base.html
│   └── variage.html
└── uploads                # Temporary storage for uploaded files
```

---

## Contributing

1. Fork this repository.
2. Create a new feature branch.
3. Commit your changes.
4. Open a pull request describing your changes.

All contributions are welcome!

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to modify and share as needed.

---

## How to Cite

If you use this application or its source code in your research, please consider citing it. For example, in APA style:

**APA (7th edition)**:
> Your Name (2025). *Whisper Audio Transcription Application* [Computer software]. GitHub.
> Retrieved from [https://github.com/your-username/whisper-audio-transcription](https://github.com/your-username/whisper-audio-transcription)

Or, in BibTeX format:

```bibtex
@misc{YourName2025,
  author       = {Your Name},
  title        = {Whisper Audio Transcription Application},
  howpublished = {\url{https://github.com/your-username/whisper-audio-transcription}},
  year         = 2025,
  note         = {Accessed: Month Day, Year}
}
