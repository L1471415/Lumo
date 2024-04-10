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

    def save_audio_samples(self, audio_samples, sample_rate=16000):
        self.audio_files = []
        
        audio_num = 0
        for audio_sample in audio_samples:
            audio_file = f"./files/voice_samples/{self.user_id}_{audio_num}_voice.wav"
            
            self.audio_files.append(audio_file)

            wavfile.write(audio_file, sample_rate, audio_sample)

            audio_num += 1

        return self

class Users:
    def __init__(self):
        self.users = {}

    def add_user(self, user:User):
        self.users[user.user_id] = user

    def get_user_by_id(self, id:str):
        return self.users[id]

    def get_id_from_name(self, name:str):
        for user_id, user in self.users.items():
            if user.name == name:
                return user_id
        
        return None

    def get_id_from_number(self, number:str):
        for user_id, user in self.users.items():
            if user.phone_number == number:
                return user_id

        return None
        
    def contains_number(self, number:str):
        for user_id, user in self.users.items():
            if user.phone_number == number:
                return True

        return False

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