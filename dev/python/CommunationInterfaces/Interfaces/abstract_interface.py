# System imports
from typing import Any

# External imports

# User imports

##########################################################

class AbstractInterface:

    def _setup(self):
        """
        Виртуальная функция для настройки
        интерфейса связи
        """
        pass

    def send_data(self, data: dict[str, Any]):
        """
        Виртуальная функция для отправки данных
        по интерфейсу связи
        """
        pass

    def receive_data(self):
        """
        Виртуальная функция для приёма данных
        по интерфейсу связи
        """
        pass