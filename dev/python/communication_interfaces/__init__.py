"""
Пакет для реализации отправки данных по интерфейсам связи
"""

__version__ = '1.0.0'
__author__ = 'Roman Romanovskiy'

# --------------------------------------------------------

from .report_sender import ReportSender
from .run_report_sender import run_report_sender

from . import Interfaces
from .Interfaces import *

# --------------------------------------------------------

__all__ = list(
    set(Interfaces.__all__) |
    {"ReportSender",
     "run_report_sender"}
)

# --------------------------------------------------------
