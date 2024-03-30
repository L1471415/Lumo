import twilio.rest as twilio
from twilio.twiml.messaging_response import MessagingResponse

from config.users import User
from config.config_variables import api_credentials, name, contacts, users, phone_number
from new_server_architecture.brain import Brain

class Contacts:
    def __init__(self, contact_list=[]):
        self.contacts_by_name = {}
        self.contacts_by_number = {}

        for number in contact_list:
            names = contact_list[number]

            if not users.contains_number(number):
                users.add_user(User(names[0], 0).add_phone_number(number))

            for name in names:
                name = name.lower()

                if not name in self.contacts_by_name.keys():
                    self.contacts_by_name[name] = number
                if not number in self.contacts_by_number.keys():
                    self.contacts_by_number[number] = name

    def get_number_from_name(self, name:str):
        return self.contacts_by_name[name.lower()]
    
    def get_name_from_number(self, number:str):
        return self.contacts_by_number[number].title()

    # Check if the number is in the contact numbers, or the lowercase name is in the contact names
    def __contains__(self, key):
        return key in self.contacts_by_number.keys() or key.lower() in self.contacts_by_name.keys()

class TwilioController:
    def __init__(self, brain:Brain):
        self.client = twilio.Client(api_credentials["twilio"]["sid"], api_credentials["twilio"]["auth_token"])

        self.brain = brain

        self.contact_list = Contacts(contact_list=contacts)

    def send_text(self, contact_name, message):
        self.client.messages.create(
            from_=phone_number,
            body="\n".join(message.splitlines()),
            to=self.contact_list.get_number_from_name(contact_name)
        )

        self.brain.append_message(message, "assistant", contact_name)
    
    def respond_to_text(self, request):
        contact_number = request.values["From"]
        if not contact_number in self.contact_list:
            return

        contact_id = users.get_id_from_number(contact_number)

        for line in self.brain.make_request(messageBody=request.values["Body"], room_name="dorm", user=contact_id):
            if line["role"] == "image":
                self.client.messages.create(
                    from_=phone_number,
                    media_url=f"{self.ngrok_url}/image?image={line['content']}",
                    to=contact_number
                )
            else:
                self.client.messages.create(
                    from_=phone_number,
                    body=line['content'],
                    to=contact_number
                )
        
    def update_url(self, url):
        self.ngrok_url = url
        self.client.incoming_phone_numbers.list(phone_number=phone_number)[0].update(sms_url=url + '/sms')