'''Module for transciribing audio into text using openai's Whisper'''

import io

from torch import cuda

from faster_whisper import WhisperModel
from openai import OpenAI as OpenAIClient
from pydub import AudioSegment

from audio.handling import SpeechSegment

from config.config_variables import api_credentials


is_local = False
prompt = "The transcript is a request to an AI assistant named Lumo"

local_model = None
openai_client = None


def get_available_device() -> str:
    '''Returns a string representing the device to run the whisper model on if local

        Returns (string):
            "cuda" if cuda-compatible nvidia gpu is detected
            "cpu" if no cuda-compaatible gpu is detected
    '''
    return "cuda" if cuda.is_available() else "cpu"


def transcribe(audio:SpeechSegment) -> str:
    '''Function to return the transcription of the supplied audio

        Parameters:
            audio (SpeechSegment): The speech segment containing the raw audio data to transcribe

        Returns (str):
            The transcription of the supplied audio
    '''

    global local_model, openai_client

    audio_segment = AudioSegment(
        data=audio.as_bytes(),
        sample_width=2,
        frame_rate=16000,
        channels=1
    )

    with io.BytesIO() as fake_file:
        fake_file.name = "dictate.wav"
        audio_segment.export(fake_file, format="wav")
        fake_file.seek(0)

        if is_local:
            if not local_model or local_model.model.device != get_available_device():
                local_model = WhisperModel("distil-large-v3", device=get_available_device())

            segments, _ = local_model.transcribe(fake_file, initial_prompt=prompt)

            return "".join(segments)
        else:
            if not openai_client:
                openai_client = OpenAIClient(api_key=api_credentials["openai"]["key"])

            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=fake_file,
                prompt=prompt
            )

            return transcript.text
