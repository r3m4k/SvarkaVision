# System imports
from typing import Any

# External imports

# User imports
from .abstract_interface import AbstractInterface

##########################################################

class CAN(AbstractInterface):
    """
    Реализация CAN интерфейса связи
    """

    def send_data(self, data: dict[str, Any]):
        print('CAN interface')