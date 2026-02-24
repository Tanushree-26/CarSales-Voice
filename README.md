# CarSales-Voice Assistant 🚗🎙️

An AI-powered voice assistant for car sales, built with Streamlit, OpenAI Whisper, Google Gemini, and ElevenLabs.

## Features
- **Voice-to-Text**: Uses OpenAI Whisper (base model) for real-time transcription.
- **Smart Recording**: Automatically detects when you stop speaking.
- **AI Brain**: Powered by Google Gemini 1.5 Flash for expert car sales advice.
- **Text-to-Speech**: High-quality voice responses using ElevenLabs.
- **Premium UI**: Clean and modern Streamlit interface.

## Prerequisites
- Python 3.9+
- [Google AI Studio API Key](https://aistudio.google.com/)
- [ElevenLabs API Key](https://elevenlabs.io/)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd CarSales-Voice
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: On Windows, you might need to install `pyaudio` via `pip install PyAudio` (may require build tools) or use `conda`.*

3. Set up environment variables:
   Copy `.env.example` to `.env` and add your API keys:
   ```bash
   GOOGLE_API_KEY=your_key_here
   ELEVENLABS_API_KEY=your_key_here
   ```

## Running the App
```bash
streamlit run app.py
```

## How it Works
1. Click **"Start Speaking"**.
2. Speak your car-related query.
3. The system detects silence when you finish.
4. Whisper transcribes your voice.
5. Gemini generates a sales-oriented response.
6. ElevenLabs converts the response to audio and plays it automatically in your browser.
