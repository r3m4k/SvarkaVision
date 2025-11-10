# System imports
from typing import Any

# External imports

# User imports
from .abstract_interface import AbstractInterface

##########################################################

class TCPServer(AbstractInterface):
    """
    Реализация интерфейса связи, как TCP сервера
    """
    def send_data(self, data: dict[str, Any]):
        print('TCP server')