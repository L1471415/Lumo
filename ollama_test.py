''' Module containing classes handling textual interactions with LLMs'''

import time
import ollama
from openai import OpenAI

from config.config_variables import api_credentials

class ChatHistory:
    '''Class which stores chat history for each user
        automatically removes the oldest messages to fit maximum context size
    '''

    def __init__(self, history_length:int=15, initial_prompts:list=None):
        self._chat_history = {}

        self._initial_prompts = []
        if initial_prompts:
            self._initial_prompts = initial_prompts

        self._max_history_length = history_length

    def append(self, message:dict, user:str=None):
        '''Add a message to the chat history of the user,
            automatically shrinking history length to the max size

            Parameters:
                message (dict): A dict containing role and content
                user (str): The name of the user to save the chat history for

            Returns: None
        '''
        if not user in self._chat_history:
            self._chat_history[user] = self._initial_prompts

        self._chat_history[user].append(message)

        while len(self._chat_history[user]) > self._max_history_length:
            del self._chat_history[user][len(self._initial_prompts)]

    def __getitem__(self, user):
        return self._chat_history[user]

class LumoChatManager:
    '''Class which handles memory, chat, and command calling when talking with Lumo'''
    def __init__(self, model_name="llama3", history_length=15, initial_prompts:list=None):
        self._model_name = model_name
        self._chat_history = ChatHistory(history_length, initial_prompts)

        if model_name == "gpt-3.5":
            self._openai = OpenAI(api_key=api_credentials["openai"]["key"])

    def chat(self, message:str, user=None):
        '''Function to send a chat message to the voice assistant

            Parameters:
                message (str): The message to send to the LLM
                user (str): The name of the user the LLM is chatting with

            Returns:
                Iterator of responses the voice assistant should read out (str)

        '''
        for _line in self._prompt_llm(message, user):
            response_line = self._parse_line_for_command(_line, user)

            yield response_line["content"]

            self._chat_history.append(response_line, user)

    def _parse_line_for_command(self, line:str, user=None):
        '''Function to parse a line of a llm response, 
            find any command, format it correctly, and call the appropriate function
            
            Parameters:
                line (str): The line (from an LLM) to parse for included commands
                user (str): The name of the user the LLM is chatting with

            Returns:
                Dict containing role and content, to be able to be saved as llm chat history:
                 {"role": "role_name", "content": "response"}
        '''
        # Commands should all have > as the first character
        if line[0] != ">":
            return {"role": "assistant", "content": line}

        command_args = line.split(" ")

        if len(command_args[0]) == 1:
            # Remove first arg if it is just the > symbol
            del command_args[0]
        else:
            # First arg includes the > symbol, so remove it
            command_args[0] = command_args[1:]

        #The command name will be the first arg, so save it seperately
        command_name = command_args.pop(0)

        # Begin at the first arg, and concat all args with a " into one element
        cur_index = 0
        while len(command_args) > cur_index:
            if '"' in command_args[cur_index]:
                if command_args[cur_index].count("\"") == 1:
                    # Only one " present in this spot, need to concat until the next one
                    while len(command_args) > cur_index+1 and not '"' in command_args[cur_index+1]:
                        command_args[cur_index] += " " + command_args[cur_index+1]
                        del command_args[cur_index+1]

                    command_args[cur_index] += " " + command_args[cur_index+1]
                    del command_args[cur_index+1]
                command_args[cur_index] = command_args[cur_index][1:-1]

            cur_index += 1

        # Find the command to call and run the function, returning the result as a chat history dict
        match command_name:
            case "get_time":
                print("TIME")

                return {"role": "system", "content": "The current time is <TIME>"}
            case "get_weather":
                print("WEATHER")

                return {"role": "system", "content": "The current weather is <WEATHER>"}

    def _prompt_llm(self, message:str, user=None):
        '''Function to prompt the llm, automatically handling chat-gpt vs ollama

            Parameters:
                message (str): The message to send to the LLM
                user (str): The name of the user the LLM is chatting with

            Returns:
                Iterator of lines the LLM responds with

        '''

        # Get the current date time in WWW YYYY-MM-DD HH:MM:SS format (eg Sat 2024-06-22 13:42)
        # Allows language model to know the date and user without needing to run a command
        timestamp = time.strftime("%a %Y-%m-%d %H:%M:%S", time.localtime())

        if user is None:
            message_stamp = f"Unknown @ {timestamp}:"
        else:
            message_stamp = f"{user.title()} @ {timestamp}:"

        chat_message = message_stamp + message

        self._chat_history.append({"role": "user", "content": chat_message}, user)

        if self._model_name == "gpt-3.5":
            #Not self hosted, so make a call to openAI instead
            openai_chat_completion = self._openai.chat.completions.create(
                    model="ft:gpt-3.5-turbo-0125:lumo:lumo:90IhRgoL",
                    messages=self._chat_history[user]
            )

            lines = openai_chat_completion.choices[0].message.content.splitlines()

            yield from lines
        else:
            # Pass the chat history (including most recent user message) to the LLM
            # The LLM will generate token by token in an iterator, so need to concat to lines
            _line = ""
            for _token in self._prompt_ollama(self._chat_history[user]):
                _line += _token

                # TODO: Should use smarter line detection, in case a command includes a \n char
                if "\n" in _token:
                    yield _line
                    _line = ""

            yield _line

    def _prompt_ollama(self, messages:list):
        '''Function to prompt the ollama model

            Parameters:
                    messages (list): A list of dict objects containing message content and role

            Returns:
                    An iterator of response tokens (string iterator)
        '''
        for _token in ollama.chat(
            model=self._model_name,
            messages=messages,
            stream=True
        ):
            yield _token["message"]["content"]


if __name__ == "__main__":
    lumo_chat_manager = LumoChatManager(initial_prompts=[])

    while True:
        for m_line in lumo_chat_manager.chat(input("Luke: "), "Luke"):
            print(m_line)
