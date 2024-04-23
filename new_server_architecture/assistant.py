import asyncio
import elevenlabs
from elevenlabs.client import ElevenLabs
import time
import requests
import threading

from config.config_variables import api_credentials, name
from audio.audio_stream import AudioHandler
from config.setup import record_user_sample

assistant_voice = {
    "luma": "nmVu5pKR445tWxY6JPEF",
    "lumo": "PWVNbNOu8k3hfTOGzHaX"
}

elevenlabs_client = ElevenLabs(api_key=api_credentials["elevenlabs"]["key"])

class Assistant:
    def __init__(self, mode="audio", voice="lumo", room="none"):
        self.mode = mode
        self.last_valid_request = None
        self.voice = elevenlabs.Voice(
            voice_id=assistant_voice[voice],
            settings=elevenlabs.VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
        )
        self.room = room

        self.gui = None

        self.audio_handler = AudioHandler()

        threading.Thread(target=self.start).start()

    def set_server(self, server):
        self.server_ip = f"{server[0]}:{server[1]}"

    def start(self):
        if self.mode == "audio":
            for audio in self.audio_handler.transcription_stream():
                response = requests.post(f"http://{self.server_ip}/process_audio", data=audio)                
                # self.gui.send_prompt(response["text"])

                self.makeRequest(response.json()["text"], response.json()["user"])
                
        if self.mode in ["read", "text"]:
            while True:
                text = input(f"{name}: ")
                self.makeRequest(text, name)      

    def makeRequest(self, text, user_id):
        response = requests.post(f"http://{self.server_ip}/make_request", data={
            "message": text,
            "user": user_id,
            "room": self.room,
            "mode": "async"
        })

    def read(self, role, content):
        if role == "image":
            try:
                print(f"http://{self.server_ip}/image?image={content}")
            except Exception as e:
                print(e)
        elif role == "voice_id":
            print("VOICE_ID-ing")
            self.audio_handler.paused = True

            name, create_new, audio_clips = record_user_sample()

            self.audio_handler.paused = False

            requests.post(f"http://{self.server_ip}/save_voice", json={
                "user_name": name,
                "create_new": create_new,
                "audio_samples": audio_clips
            })
        else:
            print(f"Lumo: {content}")
            # self.gui.send_response(text)

            if self.mode in ["read", "audio", "calibrate"]:
                audio = elevenlabs_client.generate(
                    text=content,
                    voice=self.voice,
                    model="eleven_multilingual_v2",
                    stream=True
                )
                
                elevenlabs.stream(audio)
        
        self.audio_handler.last_sent_time = time.time()
