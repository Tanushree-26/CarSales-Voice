import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

class TTSHandler:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(api_key=self.api_key)

    def text_to_speech_stream(self, text):
        """
        Generates audio from text using ElevenLabs API in a streaming fashion.
        """
        response = self.client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB", # Adam voice
            optimize_streaming_latency="0",
            output_format="mp3_44100_128",
            text=text,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.8,
                style=0.0,
                use_speaker_boost=True,
            ),
        )
        return response

    def save_audio(self, response, filename="response.mp3"):
        with open(filename, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)
        return filename
