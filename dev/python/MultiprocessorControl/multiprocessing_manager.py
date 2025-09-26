# System imports
from threading import Thread
from time import sleep
from typing import Type

from queue import Queue as ThreadQueue
from multiprocessing import Process, Queue as ProcessQueue, Pipe

# External imports

# User imports
from .multiprocessing_worker import MultiprocessingWorker
from .utils import run_in_new_process, run_mlt_worker
from .message import MessageMode, Message

##########################################################

class MultiprocessingManager:
    """
    Базовый менеджер с функционалом для взаимодействия с работником, работающий в дочернем процессе,
    и для взаимодействия с основным циклом программы, который запущен в этом же процессе.
    """
    def __init__(self):

        # Работник, с которым взаимодействует менеджер
        self._worker: Type[MultiprocessingWorker] = MultiprocessingWorker

        # Очередь поступивших команд для выполнения из основного потока
        self._command_queue: ThreadQueue[str] = ThreadQueue()

        # Поток, в котором будет осуществляться проверка наличия новых команд
        self._command_checker: Thread = Thread(target=self._command_checking, args=(), daemon=True)

        # Создание инструментов коммуникации с работником
        self._process = Process()                               # Процесс, в котором будет запущен работник
        self._msg_queue: ProcessQueue[str] = ProcessQueue()     # Очередь поступивших сообщений от работника
        self._worker_queue: ProcessQueue[str] = ProcessQueue()  # Очередь для отправки команд работнику

        # Необходимые флаги
        self._command_checking_flag: bool = True
        self._cleanup_done_flag = False

    def __del__(self):
        if not self._cleanup_done_flag:
            self.cleanup()

    def _setup(self):
        self._command_checker.start()
        self._process = run_in_new_process(run_mlt_worker, self._worker, self._worker_queue, self._msg_queue)

    def cleanup(self):
        """ Явный метод отчистки использованных ресурсов """
        self._cleanup_done_flag= True
        self._command_checking_flag = False

        self._worker_queue.put('cleanup')
        self._command_checker.join()

    def new_command(self, command: str):
        """ Отработка поступления новой команды """
        self._command_queue.put(command)

    def _command_checking(self):
        """ Функция для проверки очереди команд """
        while self._command_checking_flag:
            if not self._command_queue.empty():
                self._requests_handler(self._command_queue.get())
            else:
                sleep(1)

    def _requests_handler(self, request: str):
        pass