# CarSales-Voice Assistant 🚗🎙️

An AI-powered voice assistant for car sales, built with Streamlit, ElevenLabs Scribe v2, Google Gemini 2.0, and ElevenLabs TTS.

## Features
- **Advanced Voice-to-Text**: Uses **ElevenLabs Scribe v2** for high-accuracy, multilingual-capable (restricted to English) transcription.
- **Smart Recording**: Automatically detects silence after 3 seconds of pause, with a 60-second safety window.
- **Context-Aware AI**: Powered by **Google Gemini 2.0 Flash** with conversation history for personalized assistance.
- **Privacy-First Audio**: High-quality voice responses are streamed directly to the browser from memory (no audio files saved to disk).
- **English-Only Focus**: System is optimized to process and respond strictly in English for a consistent brand voice.
- **Premium UI**: Clean, modern, and dark-themed Streamlit interface.

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
   *Note: On Windows, you might need to install `pyaudio` via `pip install PyAudio` (may require build tools) or use `conda`. You also need `sounddevice` and `scipy`.*

3. Set up environment variables:
   Create a `.env` file in the root directory and add your API keys:
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
3. The system waits for a 3-second silence to finish recording.
4. **ElevenLabs Scribe v2** transcribes your voice into English.
5. **Gemini 2.5 Flash** generates a sales-oriented response considering the current context.
6. **ElevenLabs TTS** converts the response to audio and plays it automatically without saving any files to disk.
7. Text and voice are delivered simultaneously for a seamless experience.

## 🚀 Future Improvements

| Improvement | Description |
| :--- | :--- |
| **Live Voice Chatbot** | Transition to a fully autonomous, continuous listening mode. This will eliminate the need to click the "Start" button for every interaction, allowing for a natural, hands-free conversation flow. |
| **Real-time Inventory Access** | Integration with live dealership databases to provide instant pricing and availability of vehicles. |

