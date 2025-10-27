"""
Пакет для используемых утилит во всём проекте
"""

__author__ = 'Roman Romanovskiy'

# --------------------------------------------------------

from .singleton import singleton
from .settings_manager import SettingsManager
from .logger import Logger
from .messages_to_main import MessagesToMain
from .setup_project import setup_project
from .end_of_program import enf_of_program

# --------------------------------------------------------

__all__ = [
    'singleton',
    'Logger',
    'MessagesToMain',
    'SettingsManager',
    'setup_project',
    'enf_of_program'
]

# --------------------------------------------------------
