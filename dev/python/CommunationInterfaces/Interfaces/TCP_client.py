# System imports
from typing import Any

# External imports

# User imports
from .abstract_interface import AbstractInterface

##########################################################

class TCPClient(AbstractInterface):
    """
    Реализация интерфейса связи, как TCP клиента
    """
    def send_data(self, data: dict[str, Any]):
        print('TCP client')