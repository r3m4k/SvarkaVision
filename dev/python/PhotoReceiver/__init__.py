"""
Пакет для приёма фотографий и последующей их отправки на анализ нейронной сети
"""

__version__ = '1.0.0'
__author__ = 'Roman Romanovskiy'

# --------------------------------------------------------

from .photo_source import PhotoSource, SourceStatus
from .photo_receiver import PhotoReceiver

# --------------------------------------------------------

__all__ = [
    'PhotoSource',
    'SourceStatus',

    'PhotoReceiver'
]

# --------------------------------------------------------
