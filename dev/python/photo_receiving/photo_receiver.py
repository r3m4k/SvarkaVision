# System imports
import asyncio
import socket
from threading import Thread
import logging

# External imports

# User imports
from utils import SettingsManager, Logger
from multiprocessor_control import MultiprocessingWorker
from messages import Message, MessageMode
from .photo_source import PhotoSource

##########################################################

class PhotoReceiver(MultiprocessingWorker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server: socket.socket
        # self._photo_source: PhotoSource = PhotoSource()

    # --------------------------------
    # Основные методы класса
    # --------------------------------
    def cleanup(self):
        # self._photo_source.cleanup()    # Завершим работу источника фотографий
        # self.server.close()             # Завершим работу TCP сервера

        # Отправим сообщение о корректном завершении работы
        self._new_message(Message(MessageMode.LogInfo, "Cleanup in PhotoReceiver is done"))
        self._logger.debug(f'cleanup done, self._foo_index = {self._foo_index}')

        # Вызовем отчистку у родительского класса
        super().cleanup()

    def _setup(self):
        # Настроим TCP сервер
        # self._init_server()

        # Настроим логгер
        self._logger = Logger(
            log_filename='photo_receiver_logger',
            name='photo_receiver_logger',
            log_level=logging.DEBUG
        )

        # Добавим задачи для планировщика задач
        self._tasks.append(self._loop.create_task(self._foo_func()))

    async def _foo_func(self):
        index = 0
        while self._running_flag:
            await asyncio.sleep(1)
            index += 1
            self._new_message(Message(MessageMode.LogInfo,
                                      f'{self.__class__.__name__} -> foo_func({index})'))

    # --------------------------------
    # Методы для работы с TCP сервером
    # --------------------------------
    def _init_server(self):
        """ Настройка TCP сервера """
        # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # settings_manager = SettingsManager()
        # host = settings_manager.settings['PhotoReceiving']['host']
        # port = settings_manager.settings['PhotoReceiving']['port']
        pass

    def _requests_handler(self):
        """
        Обработчик запросов
        """
        pass

# --------------------------------------
