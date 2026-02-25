import os
import numpy as np
import sounddevice as sd
import queue
import sys
import io
from scipy.io import wavfile
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

class VoiceProcessor:
    def __init__(self):
        print("Initializing ElevenLabs Voice Processor...")
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(api_key=self.api_key)
        self.audio_queue = queue.Queue()
        self.sample_rate = 16000
        self.chunk_duration = 10  # seconds
        self.chunk_samples = int(self.sample_rate * self.chunk_duration)

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.audio_queue.put(indata.copy())

    def record_until_silence(self, silence_threshold=500, silence_duration=3.0):
        """
        Record until silence is detected.
        """
        import time
        
        print("Recording... (Speak now)")
        CHUNK = 1024
        RATE = 16000
        CHANNELS = 1
        
        audio_data = []
        silent_chunks = 0
        limit_chunks = int(silence_duration * RATE / CHUNK)
        
        # We need to record in chunks and check energy
        with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype='int16') as stream:
            while True:
                data, overflowed = stream.read(CHUNK)
                audio_data.append(data)
                
                # Check energy
                energy = np.sqrt(np.mean(data**2))
                if energy < silence_threshold:
                    silent_chunks += 1
                else:
                    silent_chunks = 0
                
                # If silent for long enough and we have some data
                if silent_chunks > limit_chunks and len(audio_data) > (RATE / CHUNK):
                    break
                
                # Safety break after 60 seconds
                if len(audio_data) > (60 * RATE / CHUNK):
                    break
        
        print("Finished recording.")
        audio_np = np.concatenate(audio_data).flatten()
        
        # Save to a bytes buffer as a WAV file
        buffer = io.BytesIO()
        wavfile.write(buffer, RATE, audio_np)
        buffer.seek(0)
        
        print("Transcribing with ElevenLabs...")
        try:
            transcription = self.client.speech_to_text.convert(
                file=buffer,
                model_id="scribe_v2", # ElevenLabs Scribe model
                tag_audio_events=True,
                language_code="eng",
                diarize=True
            )
            return transcription.text
        except Exception as e:
            print(f"Error during transcription: {e}")
            return ""

    def transcribe_file(self, file_path):
        with open(file_path, "rb") as f:
            transcription = self.client.speech_to_text.convert(
                file=f,
                model_id="scribe_v2", # Model to use
                tag_audio_events=True, # Tag audio events like laughter, applause, etc.
                language_code="eng", # Language of the audio file. If set to None, the model will detect the language automatically.
                diarize=True,
            )
            return transcription.text
