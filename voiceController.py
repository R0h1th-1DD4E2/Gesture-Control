import torch
from transformers import pipeline
import sounddevice as sd
import re
from groq import Groq
import threading
import websocket
import time

class VoiceModule:
    def __init__(self, websocket_url=None):
        if(websocket_url == None):
            print("Websocket URL is not provided.")
        else:
            self.ws = websocket.WebSocket()
            self.ws.connect(websocket_url)

        self.device = "cuda:0"
        print(self.device)
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-small.en",
            device=self.device,
        )
        print("Initializing Groq Client....")
        self.client = Groq(api_key="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")
        print("Initialized Groq Client.")

    def call_llm_function(self, text="Move forward for 2 secs and take a right and move forward for 2 secs"):
        self.commands = """
            Forward,
            Forward Right,
            Forward Left,
            Backward,
            Backward Right,
            Backward Left,
            Left,
            Right,
            Stop
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role" : "system",
                        "content" : f"You are the llm behind a bot. You have access to the following functions.{self.commands}.You will return a set of commands seperated by space and enclosed within <commands></commannds>. dont return unecessary text."
                    },
                    {
                        "role": "user",
                        "content": text,
                    }
                ],
                model="llama3-8b-8192",
                
            )
            returningResult = chat_completion.choices[0].message.content
            commands_start = returningResult.find("<commands>")
            commands_end = returningResult.find("</commands>")
            commands = returningResult[commands_start + len("<commands>"):commands_end].strip()
            commands = commands.replace('Forward', 'FWD')
            commands = commands.replace('Forward Right', 'DFRT')
            commands = commands.replace('Forward Left', 'DFLT')
            commands = commands.replace('Backward', 'BWD')
            commands = commands.replace('Backward Right', 'DWRT')
            commands = commands.replace('Backward Left', 'DWLT')
            commands = commands.replace('Left', 'LT')
            commands = commands.replace('Right', 'RT')
            commands = commands.replace('Stop', 'STP')
            commands = commands.split(' ')
            finalCommands = []
            for command in commands:
                command += ' 255 255 255 255'
                finalCommands.append(command)

            return finalCommands

        except Exception as e:
            print(e)
            print("Error occured while calling API.")




    def record_audio(self, duration=5, sample_rate=16000):
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
        sd.wait()
        print('Finished Recording Audio.')
        return audio_data.flatten()

    def get_transcription(self):
        return self.pipe(self.record_audio(), batch_size=8)


    def call_function_by_text(self, transcription):
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
            return None  # Or raise ValueError("Unrecognized command")
    

    def bot_function_string(self):
        input()
        print('Recording the voice ')
        transcription = self.get_transcription()['text'].lower()  # Convert transcription to lowercase for case-insensitivity
        commands = self.call_llm_function(text=transcription)
        print(commands)
        if(self.ws == None):
            print("Websocket is not connected.")
            return commands
        else:
            for command in commands:
                self.ws.send(command)
                time.sleep(2)
        # self.ws.send(command)

    
    def bot_llm_function(self):
        pass

voice = VoiceModule(websocket_url="ws://192.168.137.91:8080/")
while True:
    voice.bot_function_string()
