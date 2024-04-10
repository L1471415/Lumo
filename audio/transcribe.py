from openai import OpenAI
import io
from pydub import AudioSegment

from config.config_variables import api_credentials

client = OpenAI(api_key=api_credentials["openai"]["key"])

def transcribe(audio, prompt="The transcript is a request to an AI assistant named Lumo"):
    audio_segment = AudioSegment(
        data=audio,
        sample_width=2,
        frame_rate=16000,
        channels=1
    )

    with io.BytesIO() as fake_file:
        fake_file.name = "dictate.wav"
        audio_segment.export(fake_file, format="wav")
        fake_file.seek(0)

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=fake_file,
            prompt=prompt
        )

        return transcript.text