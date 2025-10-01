# System imports
from typing import TypedDict, NotRequired
from enum import Enum

# External imports

# User imports

##########################################################

class PhotoReceiverConfig(TypedDict):
    """
    Структура конфига для приёмника фотографий
    """
    host: str
    port: int
    sources_params: dict

# --------------------------------------

class QualityControllerConfig(TypedDict):
    """
    Структура конфига для алгоритма оценки качества
    сварных соединений
    """
    name: NotRequired[str]

# --------------------------------------

class ReportSenderConfig(TypedDict):
    """
    Структура конфига для модуля, отвечающего за
    отправку результатов по каналам связи
    """
    host: str
    port: int

# --------------------------------------

class AppConfig(TypedDict):
    """
    Структура конфига для всей программы
    """
    Mode: str
    LogLevel: str
    PhotoReceiving: PhotoReceiverConfig
    QualityController: QualityControllerConfig
    ReportSender: ReportSenderConfig

class AppConfigKeys(str, Enum):
    Mode = "Mode"
    LogLevel = "LogLevel"
    PhotoReceiving = "photo_receiving"
    QualityController = "QualityController"
    ReportSender = "ReportSender"

    @classmethod
    def from_string(cls, key_str: str) -> 'AppConfigKeys':
        """ Приведение строки к AppConfigKeys """
        try:
            return cls(key_str.strip())
        except ValueError:
            raise KeyError()

# --------------------------------------
