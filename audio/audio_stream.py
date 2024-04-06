import numpy as np
import time
import openwakeword
import pyaudio

import torch, torchaudio
torch.set_num_threads(1)

class VAD:
    def __init__(self):
        self.model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True,
                              onnx=False)

    def is_speaking(self, audio):
        audio_tensor = torch.tensor(audio, dtype=torch.int16).to(torch.float32)

        overall_speech_prob = 0
        window_size_samples = 512 # use 256 for 8000 Hz model
        for i in range(0, len(audio_tensor), window_size_samples):
            chunk = audio_tensor[i: i+window_size_samples]
            if len(chunk) < window_size_samples:
                break
            speech_prob = self.model(chunk, 16000).item()

            overall_speech_prob += speech_prob
            
        self.model.reset_states() # reset model states after each audio

        if(overall_speech_prob > 0.5):
            print(overall_speech_prob)

        return overall_speech_prob > 0.5

class AudioHandler:
    def __init__(self):
        self._audio_data = np.zeros((0, 1))
        self.py_audio = pyaudio.PyAudio()

        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1280

        self.vad = VAD()

    def stream(self):
        stream = self.py_audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        is_speaking = False
        start_time = 0
        end_time = 0
        last_sent_time = 0
        ready_to_send = False

        audio_data = inbuffer = np.zeros(0)

        openwakeword.utils.download_models()

        model = openwakeword.Model(["files/models/Lumo.tflite", "files/models/Hey_Lumo.tflite"])

        has_begun_speaking = False

        while True:
            indata = np.frombuffer(stream.read(self.CHUNK), np.int16)

            wake_word_predictions = model.predict(indata)

            wake_word_detected = any(val > 0.2 for val in wake_word_predictions.values())

            is_speaking = self.vad.is_speaking(indata) or wake_word_detected

            should_listen = wake_word_detected or time.time() - last_sent_time < 5

            if is_speaking:
                ready_to_send = False

                if not has_begun_speaking and should_listen:
                    print("START")
                    has_begun_speaking = True

                    audio_data = inbuffer
                    start_time = time.time()

            audio_data = np.concatenate((audio_data, indata))

            if not is_speaking:
                if not ready_to_send and has_begun_speaking:
                    end_time = time.time()
                    ready_to_send = True
                
                if ready_to_send and time.time() - end_time > 1.5:
                    yield audio_data.tobytes()

                    has_begun_speaking = False
                    ready_to_send = False
                    last_sent_time = time.time()
                    audio_data = np.zeros(0)                

            inbuffer = np.concatenate((inbuffer, indata))

            while len(inbuffer) > self.CHUNK * 20:
                inbuffer = np.delete(inbuffer, range(0, 1280))