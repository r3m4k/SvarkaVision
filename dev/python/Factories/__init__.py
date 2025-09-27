"""
Пакет реализации фабрик объектов с их сохранением
в отдельный синглтон класс
"""

__author__ = 'Roman Romanovskiy'

# --------------------------------------------------------

from .resources_storage import Resource, ResourcesStorage
from .factories import PhotoReceiverManagerFactory

# --------------------------------------------------------

__all__ = [
    'Resource',
    'ResourcesStorage',

    'PhotoReceiverManagerFactory'
]

# --------------------------------------------------------
