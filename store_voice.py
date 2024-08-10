from assistant.transcribe import StreamHandler;

import os
from config.config_variables import max_users

from mutagen.wave import WAVE
import numpy as np

from scipy.io.wavfile import write


def create_voice_profile():
    num = 0
    path = "./saved_voices"
    directory_list = os.listdir(path)

    name = input("Enter Speakers name: ")

    file_name = f"{path}/{name}'s voice.wav"
    
    StreamHandler().record(file_name)

def main():
   create_voice_profile()

if __name__ == "__main__":
    main()
