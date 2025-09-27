# System imports
from enum import Enum

# External imports

# User imports

##########################################################

class MessageMode(Enum):
    Command = "Command"
    LogInfo = "LogInfo"

    @classmethod
    def from_string(cls, key_str: str) -> 'MessageMode':
        """ Приведение строки к MessageMode """
        try:
            return cls(key_str.strip())
        except ValueError:
            raise KeyError()

# --------------------------------------

class Message:
    def __init__(self, mode: MessageMode, body: str):
        self.mode: MessageMode =  mode
        self.body: str = body
        self._separator = '__'

    def __str__(self):
        print('1')
        return self.mode.value + self._separator + self.body

    def from_string(self, str_msg: str):
        mode, msg = str_msg.split(self._separator)
        try:
            mode_enum = MessageMode.from_string(mode)
        except KeyError:
            raise RuntimeError(f"Unable to convert string {str_msg} tp Message")

        return mode_enum, msg
