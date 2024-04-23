import uuid
from scipy.io import wavfile
import json

class User:
    def __init__(self, name=None, permission_level=1, user_id:str=None, json:dict=None):
        if name:
            self.name = name
        
        self.phone_number = None
        self.audio_files = None

        if permission_level:
            self.permission_level = permission_level

        if user_id is None:
            self.user_id = str(uuid.uuid4())
        else:
            self.user_id = user_id

        if json:
            self.name = json["name"]
            self.permission_level = json["permission_level"]
            self.user_id = json["user_id"]

            self.phone_number = json["phone_number"]

            self.audio_files = json["audio_files"]        


    def add_phone_number(self, phone_number):
        self.phone_number = phone_number

        return self

    def save_audio_samples(self, audio_samples, sample_rate=16000):
        self.audio_files = []
        
        audio_num = 0
        for audio_sample in audio_samples:
            audio_file = f"./files/voice_samples/{self.user_id}_{audio_num}_voice.wav"
            
            wavfile.write(audio_file, sample_rate, audio_sample)

            self.audio_files.append(audio_file)

            audio_num += 1

        return self

class Users:
    def __init__(self):
        self.users = {}

        with open("./files/stored_data/user_info.json", 'r') as file:
            user_data = json.load(file)

            print(user_data)

            for user in user_data:
                self.users[user["user_id"]] = User(json=user)

    def add_user(self, user:User):
        self.users[user.user_id] = user

        with open("./files/stored_data/user_info.json", 'w') as file:
            user_data = []

            for user_id, user in self.users.items():
                user_data.append({
                    "name": user.name,
                    "permission_level": user.permission_level,
                    "user_id": user.user_id,
                    "phone_number": user.phone_number,
                    "audio_files": user.audio_files
                })

            print(user_data)
            
            json.dump(user_data, file)

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
    
    def contains_name(self, name):
        for user_id, user in self.users.items():
            if user.name == name:
                return True

        return False 

    def get_user_by_name(self, name):
        for user_id, user in self.users.items():
            if user.name == name:
                return user

        return None 

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

    def __str__(self):
        user_data = []

        for user_id, user in self.users.items():
            user_data.append({
                "name": user.name,
                "permission_level": user.permission_level,
                "user_id": user.user_id,
                "phone_number": user.phone_number,
                "audio_files": user.audio_files
            })

        return str(user_data)