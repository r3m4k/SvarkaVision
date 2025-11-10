# System imports
from typing import Any

# External imports

# User imports
from .abstract_interface import AbstractInterface

##########################################################

class RS485(AbstractInterface):
    """
    Реализация rs485 интерфейса связи
    """
    def send_data(self, data: dict[str, Any]):
        print('RS485 interface')