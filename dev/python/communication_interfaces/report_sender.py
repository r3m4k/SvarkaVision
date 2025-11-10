# System imports
import socket

# External imports

# User imports
from svarkaAI.report import Report
from .Interfaces import AbstractInterface

##########################################################

class ReportSender:
    """
    Класс, который отправляет данные по интерфейсам связи.
    // Реализуется через паттерн 'Наблюдатель'
    """
    def __init__(self, interfaces: list[AbstractInterface]):
        self._interfaces: list[AbstractInterface] = interfaces

    def send_report(self):
        report = {}
        for interface in self._interfaces:
            interface.send_data(report)