import numpy as np
import time
import openwakeword
import pyaudio

import torch, torchaudio
torch.set_num_threads(1)


class VAD:
    '''Class containg methods to calculte voice activity or wake word'''

    def __init__(self):
        self.model, _ = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                       model='silero_vad',
                                       force_reload=True,
                                       onnx=False)

    def calc_speech_prob(self, audio:np.ndarray) -> float:
        '''Method to calculate the probability of speech being present in the sample

            Parameters:
                audio (np.ndarray): The audio sample to calculate speech probability for

            Returns (float):
                The probability of the sample having speech [0 - 1]
        '''
        audio_tensor = torch.tensor(audio, dtype=torch.int16).to(torch.float32)

        overall_speech_prob = 0
        window_size_samples = 512  # use 256 for 8000 Hz model
        for i in range(0, len(audio_tensor), window_size_samples):
            chunk = audio_tensor[i: i + window_size_samples]
            if len(chunk) < window_size_samples:
                break
            speech_prob = self.model(chunk, 16000).item()

            if speech_prob > overall_speech_prob:
                overall_speech_prob = speech_prob

        self.model.reset_states()  # reset model states after each audio

        return overall_speech_prob

class AudioHandler:
    def __init__(self):
        self._audio_data = np.zeros((0, 1))
        self.py_audio = pyaudio.PyAudio()

        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1280

        self.last_sent_time = 0
        self.paused = False

        self.vad = VAD()

    def generic_stream(self):
        stream = self.py_audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        while True:
            if not self.paused:
                yield np.frombuffer(stream.read(self.CHUNK), np.int16)
            
    def setup_stream(self):
        is_speaking = False
        end_time = 0
        ready_to_send = False

        audio_data = extra_context_buffer = speech_detect_sample = np.zeros(0)

        has_begun_speaking = False

        for indata in self.generic_stream():
            is_speaking = self.vad.calc_speech_prob(speech_detect_sample) > 0.55

            if is_speaking:
                ready_to_send = False

                if not has_begun_speaking:
                    print("START")
                    has_begun_speaking = True

                    audio_data = extra_context_buffer
                    start_time = time.time()

            audio_data = np.concatenate((audio_data, indata))

            if not is_speaking:
                if not ready_to_send and has_begun_speaking:
                    end_time = time.time()
                    ready_to_send = True

                if ready_to_send and time.time() - end_time > 1.5:
                    yield audio_data.astype(np.int16).tobytes()

                    has_begun_speaking = False
                    ready_to_send = False
                    last_sent_time = time.time()
                    audio_data = np.zeros(0)

            speech_detect_sample = np.concatenate((speech_detect_sample, indata))

            while len(speech_detect_sample) > self.CHUNK * 20:
                speech_detect_sample = np.delete(speech_detect_sample, range(0, 1280))

            extra_context_buffer = np.concatenate((extra_context_buffer, indata))

            while len(extra_context_buffer) > self.CHUNK * 20:
                extra_context_buffer = np.delete(extra_context_buffer, range(0, 1280))

    def transcription_stream(self):
        is_speaking = False
        start_time = 0
        end_time = 0
        ready_to_send = False

        audio_data = speech_detect_sample = extra_context_buffer = np.zeros(0)

        self.model = openwakeword.model.Model(["files/models/Lumo.onnx", "files/models/Hey_Lumo.onnx"])

        has_begun_speaking = False

        for indata in self.generic_stream():
            wake_word_predictions = self.model.predict(indata)

            wake_word_detected = any(val > 0.2 for val in wake_word_predictions.values())

            is_speaking = self.vad.calc_speech_prob(speech_detect_sample.astype(np.int16)) > 0.55 or wake_word_detected

            should_listen = wake_word_detected or time.time() - self.last_sent_time < 5

            if is_speaking:
                ready_to_send = False

                if not has_begun_speaking and should_listen:
                    print("START")
                    has_begun_speaking = True

                    audio_data = extra_context_buffer
                    start_time = time.time()

            audio_data = np.concatenate((audio_data, indata))

            if not is_speaking:
                if not ready_to_send and has_begun_speaking:
                    end_time = time.time()
                    ready_to_send = True
                
                if ready_to_send and time.time() - end_time > 1:
                    yield audio_data.astype(np.int16).tobytes()

                    has_begun_speaking = False
                    ready_to_send = False
                    self.last_sent_time = time.time()
                    audio_data = np.zeros(0)

            speech_detect_sample = np.concatenate((speech_detect_sample, indata))

            while len(speech_detect_sample) > self.CHUNK * 5:
                speech_detect_sample = np.delete(speech_detect_sample, range(0, 1280))
            
            extra_context_buffer = np.concatenate((extra_context_buffer, indata))

            while len(extra_context_buffer) > self.CHUNK * 20:
                extra_context_buffer = np.delete(extra_context_buffer, range(0, 1280))
