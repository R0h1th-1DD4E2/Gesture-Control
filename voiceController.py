import torch
from transformers import pipeline
import sounddevice as sd

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

voice = VoiceModule()

while True:
    input()
    print('Recording the voice')
    print(voice.get_transcription()['text'])
