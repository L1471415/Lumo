import uuid
from scipy.io import wavfile

class User:
    def __init__(self, name, permission_level=1, user_id:str=None):
        self.name = name

        self.permission_level = permission_level

        if user_id is None:
            self.user_id = str(uuid.uuid4())
        else:
            self.user_id = user_id

    def add_phone_number(self, phone_number):
        self.phone_number = phone_number

        return self

class Users:
    def __init__(self):
        self.users = {}

    def add_user(self, user:User):
        self.users[user.user_id] = user

    def get_user_by_id(self, id:str):
        return self.users[id]

    def get_id_from_number(self, number:str):
        for user_id, user in self.users.items():
            if user.phone_number == number:
                return user_id
        
    def contains_number(self, number:str):
        for user_id, user in self.users.items():
            if user.phone_number == number:
                return True

        return False

    def save_audio_sample(self, audio_sample, sample_rate=16000):
        self.audio_file = f"./config/voice_samples/{self.user_id}_voice.wav"

        wavfile.write(self.audio_file, sample_rate, audio_sample)
        
        return self

    def __contains__(self, id):
        return id in self.users.keys()

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.users):
            user_id = list(self.users.keys())[self.index]
            self.index += 1
            return self.users[user_id]
        else:
            raise StopIteration