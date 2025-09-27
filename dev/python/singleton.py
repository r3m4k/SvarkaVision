# System imports
import threading

# External imports

# User imports

##########################################################

class Singleton:
    """
    Потокобезопасный класс для реализации паттерна Singleton
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self, *args, **kwargs):
        if not getattr(self, '_initialized', False):
            self._initialized = True
            super().__init__(*args, **kwargs)