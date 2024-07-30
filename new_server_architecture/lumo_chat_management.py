''' Module containing classes handling textual interactions with LLMs'''

import time
import copy
import ollama
from openai import OpenAI

from config_variables import api_credentials

class ChatHistory:
    '''Class which stores chat history for each user
        automatically removes the oldest messages to fit maximum context size
    '''

    def __init__(self, history_length: int=15, initial_prompts:list=None):
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

        if user not in self._chat_history:
            self._chat_history[user] = copy.deepcopy(self._initial_prompts)

        self._chat_history[user].append(message)

        while len(self._chat_history[user]) > self._max_history_length:
            del self._chat_history[user][len(self._initial_prompts)]

    def __getitem__(self, user):
        return self._chat_history[user]


class LumoChatManager:
    '''Class which handles memory, chat, and command calling when talking with Lumo'''
    def __init__(self, model_name="llama3", history_length=20, initial_prompts:list=None):
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

        user_message = self._format_user_message(message, user)

        self._chat_history.append(user_message, user)

        should_prompt_llm = True

        while should_prompt_llm:
            should_prompt_llm = False

            for _line in self._get_llm_response(self._chat_history[user], self._model_name):
                # If the line has no content, ignore it
                if not _line or len(_line.strip()) == 0:
                    continue

                self._chat_history.append({"role": "assistant", "content": _line})

                command_result = self._parse_line_for_command(_line, user)

                if command_result is None:
                    # Line wasn't a command, so yield the line as output (to be read aloud)
                    yield _line

                else:
                    if command_result["continue_response"]:
                        # Command contains content that should be context for the current response,
                        # Once this part of the response is done, the LLM should be allowed to continue
                        should_prompt_llm = True

                    if command_result["response"]:
                        # As long as the command run had a response, append it to the chat history as a system prompt
                        self._chat_history.append({"role": "system", "content": command_result["response"]}, user)

    def _parse_line_for_command(self, line:str, user=None):
        '''Function to parse a line of a llm response, 
            find any command, format it correctly, and call the appropriate function
            
            Parameters:
                line (str): The line (from an LLM) to parse for included commands
                user (str): The name of the user the LLM is chatting with

            Returns:
                Tuple of a dict with role and content, to be able to be saved as llm chat history:
                 {"role": "role_name", "content": "response"}
                Also a boolean which is True if this command should have the LLM continue responding
        '''
        if len(line) == 0:
            raise ValueError("Line must have content!")

        # Commands should all have > as the first character
        if line[0] != ">":
            return None

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
                return {
                    "response": "{'location': '<LOCATION>', 'time': '<DATETIME>'}",
                    "continue_response": True
                }

            case "get_weather":
                return {
                    "response": "{'today': {'temp': 76, 'forecast': 'mild showers'}}",
                    "continue_response": True
                }

            case "set_alarm":
                return {
                    "response": f"Set alarm <ALARM> for {user}",
                    "continue_response": False
                }

        return {
            "response": f"Command {command_name} with args {command_args} not found.",
            "continue_response": False
        }

    def _format_user_message(self, message:str, user=None):
        '''Function to generate a correctly formatted user method as a dict to save to chat history
            
            Parameters:
                message (str): The message the user sent to prompt the LLM with
                user (str): The user's name

            Returns:
                Dict containing role and content
        '''

        # Get the current date time in WWW YYYY-MM-DD HH:MM:SS format (eg Sat 2024-06-22 13:42)
        # Allows language model to know the date and user without needing to run a command
        timestamp = time.strftime("%a %Y-%m-%d %H:%M:%S", time.localtime())

        if user is None:
            message_stamp = f"Unknown @ {timestamp}:"
        else:
            message_stamp = f"{user.title()} @ {timestamp}:"

        chat_message = message_stamp + message

        return {"role": "user", "content": chat_message}

    def _get_llm_response(self, message_history:list, model:str):
        '''General function to prompt the llm, given a chat history and a model

            Parameters:
                message_history (list<str>): The message history to send to the LLM
                model (str): The name of the LLM model

            Returns:
                Iterator of lines the LLM responds with

        '''

        if model == "gpt-3.5":
            #Not self hosted, so make a call to openAI instead
            openai_chat_completion = self._openai.chat.completions.create(
                    model="ft:gpt-3.5-turbo-0125:lumo:lumo:90IhRgoL",
                    messages=message_history
            )

            lines = openai_chat_completion.choices[0].message.content.splitlines()

            yield from lines
        else:
            # Pass the chat history (including most recent user message) to the LLM
            # The LLM will generate token by token in an iterator, so need to concat to lines
            _line = ""
            for _token in self._get_ollama_response(message_history, model):
                _line += _token

                # TODO: Should use smarter line detection, in case a command includes a \n char
                if "\n" in _token:
                    yield _line
                    _line = ""

            yield _line

    def _get_ollama_response(self, messages:list, model:str):
        '''Function to prompt the ollama model

            Parameters:
                    messages (list): A list of dict objects containing message content and role
                    model (str): The model to prompt for a response

            Returns:
                    An iterator of response tokens (string iterator)
        '''
        for _token in ollama.chat(
            model=model,
            messages=messages,
            stream=True
        ):
            yield _token["message"]["content"]

if __name__ == "__main__":
    with open("./files/gpt_prompts/commands.yaml", "r", encoding="utf8") as commands:
        lumo_chat_manager = LumoChatManager(model_name="llama3", initial_prompts=[
            {"role": "system", "content": "You are Lumo, a helpful and friendly voice assistant AI. Only respond as Lumo, and never a user. As Lumo, you have a list of commands you can call by responding to a user with '> command_name', which give you added functionality. Each command must be on its own line and begin with >. A list of the commands you can call and their function is provided: "},
            {"role": "system", "content": commands.read()},
            {"role": "user", "content": "User @ Mon 2024-05-06 12:25:24:Hey Lumo, what's the weather like today?"},
            {"role": "assistant", "content": "Let me check that for you!\n> get_weather"}
        ])
