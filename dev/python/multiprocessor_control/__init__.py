"""
Пакет реализации запуска работников в отдельном процессе и
связанных с ними менеджеров для связи дочернего процесса с
основным с помощью очередей сообщений
"""

__author__ = 'Roman Romanovskiy'

# --------------------------------------------------------

from .multiprocessing_manager import MultiprocessingManager
from .multiprocessing_worker import  MultiprocessingWorker
from .message import MessageMode, Message

# --------------------------------------------------------

__all__ = [
    'MultiprocessingManager',
    'MultiprocessingWorker',

    'Message',
    'MessageMode',
]

# --------------------------------------------------------
