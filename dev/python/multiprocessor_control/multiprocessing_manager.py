# System imports
from abc import abstractmethod
from threading import Thread
from time import sleep
from typing import Type

from queue import Queue as ThreadQueue
from multiprocessing import Process, Queue as ProcessQueue

# External imports

# User imports
from factories import Resource
from messages_to_main import MessagesToMain
from .multiprocessing_worker import MultiprocessingWorker
from .utils import run_in_new_process, run_mlt_worker
from .message import MessageMode, Message

##########################################################

class MultiprocessingManager(Resource):
    """
    Базовый менеджер с функционалом для взаимодействия с работником, работающий в дочернем процессе,
    и для взаимодействия с основным циклом программы, который запущен в этом же процессе.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._worker: Type[MultiprocessingWorker] = MultiprocessingWorker       # Работник, с которым взаимодействует менеджер
        self._messages_to_main: MessagesToMain = MessagesToMain()               # Очередь сообщений в основной поток программы

        self._process = Process()                                       # Процесс, в котором будет запущен работник
        self._commands_to_worker: ProcessQueue = ProcessQueue()         # Очередь для отправки команд работнику
        self._messages_from_worker: ProcessQueue = ProcessQueue()       # Очередь поступивших сообщений от работника

        # Необходимые флаги
        self._need_to_check_commands_from_main_flag: bool = True
        self._cleanup_done_flag = False

    def __del__(self):
        if not self._cleanup_done_flag:
            self.cleanup()

    def setup(self):
        self._process = run_in_new_process(run_mlt_worker, self._worker, self._commands_to_worker, self._messages_from_worker)

    def cleanup(self):
        """ Явный метод отчистки использованных ресурсов """
        print('MultiprocessingManager --> cleanup')
        self._cleanup_done_flag= True
        self._need_to_check_commands_from_main_flag = False

        self._commands_to_worker.put('cleanup')

    def commands_executor(self, command: str):
        """ Обработка поступившей команды """
        pass