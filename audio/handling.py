'''Module containing classes for audio input and output'''

from __future__ import annotations  # Allow for type hints to be used in the class that defines the type

import numpy as np
import samplerate
import openwakeword

from audio.audio_stream import VAD


class SpeechSegment:
    '''Class containing raw audio of a segment of speech audio'''

    def __init__(self, audio_data:np.ndarray, sample_rate:int):
        if len(audio_data.shape) > 1:  # If audio is multichannel, average it to mono
            audio_data = audio_data.mean()

        if sample_rate != 16000:
            audio_data = samplerate.resample(audio_data, 16000 / sample_rate)

        self._audio_data = np.copy(audio_data)  # Copy to guarentee no reference issues

    def get_audio_array(self) -> np.ndarray:
        '''Getter function to return the numpy array of audio data

            Returns (np.ndarray):
                The numpy array containing the audio data
        '''

        return self._audio_data

    def as_bytes(self) -> bytes:
        '''Method to return the bytearray containing audio data

            Returns (bytes):
                raw audio bytes
        '''

        return self._audio_data.tobytes()

    @staticmethod
    def from_bytes(audio_bytes:bytes, sample_rate:int=16000) -> SpeechSegment:
        '''Method to construct a SpeechSegment from a bytes array,
            automatically flattening to mono and re-sampling to the desired sample-rate

            Parameters:
                audio_bytes (bytes): The bytes object containing the raw audio data
                sample_rate (int): The sample rate of the audio data

            Returns (SpeechSegment):
                SpeechSegment containing the resampled and flattened audio data
        '''

        audio_data = np.frombuffer(audio_bytes)

        return SpeechSegment(audio_data, sample_rate)


BIT_DEPTH = 16
SAMPLE_RATE = 16000


class AudioInputStream:
    '''Class to handle recieving audio bytes, appending them to the utterance,
    and detecting when speech should be stopped'''

    def __init__(self):
        self._audio_array = np.empty(0, dtype=np.int16)
        self._bytes_buffer = np.empty(0, dtype=np.int16)

        self._vad = VAD()
        self._wake_word_model = openwakeword.model.Model(["files/models/Lumo.tflite", "files/models/Hey_Lumo.tflite"])

        self._time_since_lumo_spoke = 5

        self._time_since_last_vad = 0
        self._has_begun_speaking = False

    def append_bytes(self, recieved_bytes:bytes):
        '''Method to append recieved audio to the current byte array

            Parameters:
                recieved_bytes
        '''

        self._bytes_buffer = np.concatenate((self._bytes_buffer, np.frombuffer(recieved_bytes, dtype=np.int16)))

        if len(self._bytes_buffer) > (SAMPLE_RATE) * 1:  # Trim the bytes buffer to 2 second of audio
            self._bytes_buffer = self._bytes_buffer[-(SAMPLE_RATE * 1):]

        wake_word_predictions = self._wake_word_model.predict(self._bytes_buffer)

        said_wake_word = any(val > 0.4 for val in wake_word_predictions.values())

        voice_activity_detected = self._vad.calc_speech_prob(self._bytes_buffer) > 0.7

        if not self._has_begun_speaking:
            if said_wake_word or (voice_activity_detected and self._time_since_lumo_spoke < 5):
                self._has_begun_speaking = True
                self._audio_array = np.copy(self._bytes_buffer)
                print("SPEAKING")

        else:
            self._audio_array = np.concatenate(self._audio_array, recieved_bytes)

            if voice_activity_detected:
                self._time_since_last_vad = 0

            else:
                self._time_since_last_vad += len(recieved_bytes) / SAMPLE_RATE

            if self._time_since_last_vad > 1:
                self._has_begun_speaking = False
                print("DONE")

    def is_finished(self) -> bool:
        '''Method to determine whether the user is finished speaking

            Returns (bool):
                True if finished speaking, False if not
        '''

        return not self._has_begun_speaking and len(self._audio_array) > 0

    def get_speech_segment(self) -> SpeechSegment:
        '''Method to return the last spoken segment of audio as a speech segment object

            NOTE: ALSO CLEARS THE SAVED AUDIO

            Returns (SpeechSegment):
                SpeechSegment containing last spoken audio
        '''

        audio = SpeechSegment(self._audio_array, SAMPLE_RATE)

        self._audio_array = np.empty(0)
        self._bytes_buffer = np.empty(0)

        return audio
