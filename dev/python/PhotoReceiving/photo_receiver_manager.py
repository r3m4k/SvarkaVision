# System imports

# External imports

# User imports
from MultiprocessorControl import MultiprocessingManager
from .photo_receiver import PhotoReceiver

##########################################################

class PhotoReceiverManager(MultiprocessingManager):
    """
    Класс, предназначенный для запуска приёмника фотографий
    и для управления им
    """
    def __init__(self, resource_name: str):
        super().__init__(resource_name)
        self._worker= PhotoReceiver

    def _requests_handler(self, request: str):
        pass

# --------------------------------------

def run_photo_receiver():
    pass