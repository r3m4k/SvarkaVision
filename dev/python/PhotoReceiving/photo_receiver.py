# System imports
import socket

# External imports

# User imports
from settings_manager import SettingsManager
from MultiprocessorControl import MultiprocessingWorker
from .photo_source import PhotoSource

##########################################################

class PhotoReceiver(MultiprocessingWorker):
    def __init__(self):
        self.server: socket.socket = None
        self._photo_source: PhotoSource = PhotoSource()

    def cleanup(self):
        self._photo_source.cleanup()
        self.server.close()

    def _init_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        settings_manager = SettingsManager()
        host = settings_manager.settings['PhotoReceiving']['host']
        port = settings_manager.settings['PhotoReceiving']['port']

    def _requests_handler(self):
        """
        Обработчик запросов
        """
        pass