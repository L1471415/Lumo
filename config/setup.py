import elevenlabs
from elevenlabs.client import ElevenLabs
import asyncio
from openai import OpenAI
from scipy.io import wavfile

from audio.audio_stream import AudioHandler
from audio.transcribe import transcribe
from config.config_variables import api_credentials
from config.users import User

elevenlabs_client = ElevenLabs(api_key=api_credentials["elevenlabs"]["key"])

openai = OpenAI(api_key=api_credentials["openai"]["key"])

lumo_voice = elevenlabs.Voice(
    voice_id="PWVNbNOu8k3hfTOGzHaX",
    settings=elevenlabs.VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
)

#Creating user profile via assistant
def record_user_sample(name=None):
    audio_handler = AudioHandler()

    audio_generator = audio_handler.setup_stream()

    repeat_query_audio = None
    
    if not name:
        name = "none"

        name_query_audio = b''.join(elevenlabs_client.generate(
            text="Let's begin setting up your user profile. To start, please tell me your name.",
            voice=lumo_voice,
            model="eleven_multilingual_v2"
        ))
        
        elevenlabs.play(name_query_audio)

        name_confirmed = False
        re_ask_name_audio = None

        while not name_confirmed:
            while name == "none":
                audio_sample = next(audio_generator)
                transcription = transcribe(audio_sample, prompt="The user is providing their name:")

                print(transcription)

                name = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[
                    {"role": "system", "content": "What is name the user provided in the following message. If they didn't provide a name respond with \"None\". Only respond with a single word."},
                    {"role": "user", "content": transcription}
                ]).choices[0].message.content.lower()

                if name == "none":
                    if not repeat_query_audio:
                        repeat_query_audio = b''.join(elevenlabs_client.generate(
                            text="I'm sorry, I didn't quite get that. <break time=\"0.5s\" /> Would you mind repeating it?",
                            voice=lumo_voice,
                            model="eleven_multilingual_v2"
                        ))
                    
                    elevenlabs.play(repeat_query_audio)

            user_confirm_response = "neither"

            repeat_confirm_audio = None

            name_confirm_audio = b''.join(elevenlabs_client.generate(
                text=f"Just to confirm, your name is {name}, correct?",
                voice=lumo_voice,
                model="eleven_multilingual_v2"
            ))
            while "neither" in user_confirm_response:
                elevenlabs.play(name_confirm_audio)
                
                audio_sample = next(audio_generator)
                transcription = transcribe(audio_sample, prompt="").lower()

                user_confirm_response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[
                    {"role": "system", "content": "Was the users response a confirmation (eg yes, correct, etc), a rejection (eg no, wrong, etc), or neither. Answer with only one word(confirmed, rejected, or neither)"},
                    {"role": "user", "content": transcription}
                ]).choices[0].message.content.lower()

                print(user_confirm_response)

                if "confirm" in user_confirm_response:
                    name_confirmed = True
                elif "reject" in user_confirm_response:
                    name = "none"

                    if not re_ask_name_audio:
                        re_ask_name_audio = b''.join(elevenlabs_client.generate(
                            text=f"Got it. Could you tell me your name again, please?",
                            voice=lumo_voice,
                            model="eleven_multilingual_v2"
                        ))

                    elevenlabs.play(re_ask_name_audio)
                else:
                    if not repeat_confirm_audio:
                        repeat_confirm_audio = b''.join(elevenlabs_client.generate(
                            text="I'm sorry, I didn't quite get that. Would you mind repeating it?",
                            voice=lumo_voice,
                            model="eleven_multilingual_v2"
                        ))
                    
                    elevenlabs.play(repeat_confirm_audio)
    
    create_new = True
    if True:
        user_confirm_response = "neither"

        name_confirm_audio = b''.join(elevenlabs_client.generate(
            text=f"It looks like a user with the name {name} already exists, is that you?",
            voice=lumo_voice,
            model="eleven_multilingual_v2"
        ))
        while "neither" in user_confirm_response:
            elevenlabs.play(name_confirm_audio)
            
            audio_sample = next(audio_generator)
            transcription = transcribe(audio_sample, prompt="").lower()

            user_confirm_response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[
                {"role": "system", "content": "Was the users response a confirmation (eg yes, correct, etc), a rejection (eg no, wrong, etc), or neither. Answer with only one word(confirmed, rejected, or neither)"},
                {"role": "user", "content": transcription}
            ]).choices[0].message.content.lower()

            print(user_confirm_response)

            if "confirm" in user_confirm_response:
                create_new = False
            elif "reject" in user_confirm_response:
                create_new = True
            else:
                if not repeat_confirm_audio:
                    repeat_confirm_audio = b''.join(elevenlabs_client.generate(
                        text="I'm sorry, I didn't quite get that. Would you mind repeating it?",
                        voice=lumo_voice,
                        model="eleven_multilingual_v2"
                    ))
                
                elevenlabs.play(repeat_confirm_audio)

    text_examples = ["Hey Lumo, what's the weather like today?", "Hey Lumo, can you turn off the lights in the Living Room?"]
    audio_clips = []

    first_prompt_audio = b''.join(elevenlabs_client.generate(
        text=f"Hello {name}! <break time=\"0.5s\"> Let's begin recording some voice samples.",
        voice=lumo_voice,
        model="eleven_multilingual_v2"
    ))

    elevenlabs.play(first_prompt_audio)

    for text_example in text_examples:
        reprompt_audio = None

        text_prompt_audio = b''.join(elevenlabs_client.generate(
            text=f"Please repeat the following: {text_example}",
            voice=lumo_voice,
            model="eleven_multilingual_v2"
        ))

        elevenlabs.play(text_prompt_audio)

        prompt_finished = False
        while not prompt_finished:
            audio_sample = next(audio_generator)
            transcription = transcribe(audio_sample).lower()

            print(transcription)

            if transcription.replace(".", "").replace(",", "") == text_example.lower().replace(".", "").replace(",", ""):
                prompt_finished = True
                audio_clips.append(audio_sample)
            else:
                if not reprompt_audio:
                    reprompt_audio = b''.join(elevenlabs_client.generate(
                        text=f"I'm sorry, I didn't quite get that. Please repeat the following: {text_example}",
                        voice=lumo_voice,
                        model="eleven_multilingual_v2"
                    ))
                
                elevenlabs.play(reprompt_audio)

    finished_audio = b''.join(elevenlabs_client.generate(
        text=f"Great! I've finished learning your voice. In the future, your voice will be associated with your user profile.",
        voice=lumo_voice,
        model="eleven_multilingual_v2"
    ))
                
    elevenlabs.play(finished_audio)

    return name, create_new, audio_clips