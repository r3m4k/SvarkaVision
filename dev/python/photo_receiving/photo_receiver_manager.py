# System imports

# External imports

# User imports
from multiprocessor_control import MultiprocessingManager
from .photo_receiver import PhotoReceiver

##########################################################

class PhotoReceiverManager(MultiprocessingManager):
    """
    Класс, предназначенный для запуска приёмника фотографий
    и для управления им
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._worker = PhotoReceiver

# --------------------------------------
