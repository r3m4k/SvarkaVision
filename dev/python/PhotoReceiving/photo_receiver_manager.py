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
    def __init__(self):
        super().__init__()
        self._resource: PhotoReceiver = PhotoReceiver()

# --------------------------------------

def run_photo_receiver():
    pass