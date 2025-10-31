"""
Пакет для программной реализации поддерживаемых интерфейсов связи
"""

__version__ = '1.0.0'
__author__ = 'Roman Romanovskiy'

# --------------------------------------------------------

from .abstract_interface import AbstractInterface
from .CAN_interface import CAN
from .RS485_interface import RS485
from .TCP_server import TCPServer
from .TCP_client import TCPClient

# --------------------------------------------------------

__all__ = [
    "AbstractInterface",
    "CAN",
    "RS485",
    "TCPServer",
    "TCPClient"
]

# --------------------------------------------------------
