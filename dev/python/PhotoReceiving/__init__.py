"""
Пакет для приёма фотографий и последующей их отправки на анализ нейронной сети
"""

__author__ = 'Roman Romanovskiy'

# --------------------------------------------------------

from .photo_source import PhotoSource, SourceStatus
from .photo_receiver import PhotoReceiver
from .photo_receiver_manager import PhotoReceiverManager

# --------------------------------------------------------

__all__ = [
    'PhotoSource',
    'SourceStatus',

    'PhotoReceiver',
    'PhotoReceiverManager'
]

# --------------------------------------------------------
