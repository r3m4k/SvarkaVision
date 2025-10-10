# System imports
import socket
from threading import Thread
from time import sleep

# External imports

# User imports
from settings_manager import SettingsManager
from multiprocessor_control import MultiprocessingWorker
from messages import Message, MessageMode
from .photo_source import PhotoSource

##########################################################

class PhotoReceiver(MultiprocessingWorker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server: socket.socket = None
        self._photo_source: PhotoSource = PhotoSource()

        self._foo_index: int = 0

    def cleanup(self):
        super().cleanup()               # Вызовем отчистку у родительского класса

        self._photo_source.cleanup()    # Завершим работу источника фотографий
        # self.server.close()             # Завершим работу TCP сервера

        # Отправим сообщение о корректном завершении работы
        self.new_message(Message(MessageMode.LogInfo, "Cleanup in PhotoReceiver is done"))

    def _setup(self):
        # self._init_server()

        # Тут надо запустить планировщик задач
        self._executors.append(
            Thread(target=self._foo_func, args=(), daemon=True)
        )

    def _foo_func(self):
        while self._working_in_subthreads:
            self._foo_index += 1
            self.new_message(Message(MessageMode.LogInfo, f"Tick #{self._foo_index}"))

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

# --------------------------------------
