from openai import OpenAI
import io
from pydub import AudioSegment

from config.config_variables import api_credentials

client = OpenAI(api_credentials["openai"]["key"])

def transcribe(audio):
    audio_bytes = audio.astype(np.int16).tobytes()

    audio_segment = AudioSegment(
        data=audio_bytes,
        sample_width=2,
        frame_rate=16000,
        channels=1
    )

    with io.BytesIO() as file:
        file.name = "dictate.wav"
        audio_segment.export(file, format="wav")
        file.seek(0)

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            prompt="The transcript is a request to an AI assistant named Lumo"
        )

        return transcript.text