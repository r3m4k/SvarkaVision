"""
Пакет для работы алгоритма машинного зрения и анализа качества сварных швов
"""

__version__ = '1.0.0'
__author__ = 'Roman Romanovskiy, Alexander Sanzhapov'

# --------------------------------------------------------

from .report import (
    Picture,
    DefectStatus,
    Report
)

# --------------------------------------------------------

__all__ = [
    # from .report
    'Picture',
    'DefectStatus',
    'Report'

]

# --------------------------------------------------------
