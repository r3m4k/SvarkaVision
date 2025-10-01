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
    def __init__(self, resource_name: str, **kwargs):
        super().__init__(resource_name)
        self._worker= PhotoReceiver

# --------------------------------------

def run_photo_receiver():
    pass