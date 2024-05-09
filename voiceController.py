import torch
from transformers import pipeline
import sounddevice as sd
import re

class VoiceModule:
    def __init__(self):
        self.device = "cuda:0"
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-small.en",
            device=self.device,
        )

    def record_audio(self, duration=1.4, sample_rate=16000):
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
        sd.wait()
        return audio_data.flatten()

    def get_transcription(self):
        return self.pipe(self.record_audio(), batch_size=8)


    def bot_function_string(self):
        input()
        print('Recording the voice ')
        transcription = self.get_transcription()['text'].lower()  # Convert transcription to lowercase for case-insensitivity
        

        if "forward" in transcription:
            if "right" in transcription:
                return "DFRT"  # Forward Right
            elif "left" in transcription:
                return "DFLT"  # Forward Left
            else:
                return "FWD"   # Forward
        elif "backward" in transcription:
            if "right" in transcription:
                return "DWRT"  # Backward Right
            elif "left" in transcription:
                return "DWLT"  # Backward Left
            else:
                return "BWD"   # Backward
        elif "left" in transcription:
            return "LT"   # Left
        elif "right" in transcription:
            return "RT"   # Right
        elif "stop" in transcription:
            return "STP"  # Stop
        elif "change" in transcription:
            return f"PWM {0} {0} {0} {0}"
        else:
            # If no movement command is recognized, return None or raise an exception
            return None  # Or raise ValueError("Unrecognized command")


voice = VoiceModule()

while True:
    print("Command : " ,voice.bot_function_string())