import uuid

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

    def __contains__(self, id):
        return id in self.users.keys()