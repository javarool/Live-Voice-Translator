# Live Voice Translator

## Project Description

**Live Voice Translator** is a real-time speech translation project built using the following components:

- **Fast Whisper** — a deep learning model for speech recognition.
- **LibreTranslate** — an API for translating text from one language to another.
- **Paper-TTS** — a module for text-to-speech synthesis.

The project supports translating from any language to English, with the option to select the source language. Speech processing and translation are handled asynchronously, allowing for minimal latency during translation. The system leverages GPU acceleration, requiring a graphics card with 4 to 8 GB of memory.

## Key Features

- **Speech Recognition:** Fast and accurate speech recognition using Fast Whisper.
- **Text Translation:** Multilingual text translation supported via LibreTranslate.
- **Speech Synthesis:** Convert translated text into speech using Paper-TTS.
- **Asynchronous Processing:** Uses asynchronous threads for parallel processing of recognition, translation, and speech synthesis.
- **GPU Support:** Accelerated computations using GPU for faster processing.

## Requirements

- **Python 3.8+**
- **CUDA 10.1+** (for GPU support)
- **A CUDA-compatible GPU** with 4 to 8 GB of memory
- **Dependencies:** 
https://github.com/LibreTranslate/LibreTranslate
More Voices https://github.com/rhasspy/piper/blob/master/VOICES.md
Additionally, the project requires access to the LibreTranslate service for translation. You can either:

Deploy LibreTranslate locally: Follow the instructions on the LibreTranslate GitHub page to set up the service.
Use a cloud-based LibreTranslate API: Sign up and obtain an API key from a cloud service that offers LibreTranslate.

Install the required libraries by running the following command:
```bash
git clone https://github.com/yourusername/live-voice-translator.git
pip install -r requirements.txt
python main.py
