# System imports
import threading
from abc import abstractmethod
import sys
from multiprocessing import Queue as ProcessQueue
from threading import Thread, current_thread
from typing import Callable
import signal

# External imports

# User imports
from messages import Message
from consts import signals

##########################################################

class MultiprocessingWorker:
    """
    Базовый класс, для создания объекта, который будет выполняться
    в отдельном процессе и поддерживающий двустороннюю коммуникацию
    с основным процессом через очереди команд и сообщений.

    Также автоматически выполняет очистку ресурсов при удалении объекта.
    """

    def __init__(self, command_queue: ProcessQueue, message_queue: ProcessQueue):
        self._command_queue = command_queue     # Очередь поступивших команд из основного процесса
        self._message_queue = message_queue     # Очередь для отправки сообщений в основной процесс

        self._executors: list[Thread] = list()    # Список дополнительных потоков

        # Необходимые флаги
        self._cleanup_done_flag: bool = False
        self._working_in_subthreads: bool = False

    def __del__(self):
        if not self._cleanup_done_flag:
            self.cleanup()

    def cleanup(self):
        """ Явный метод отчистки """
        self._working_in_subthreads = False
        for thread in self._executors:
            if thread.is_alive() and thread.ident != current_thread().ident:
                thread.join()

    def start(self):
        """ Метод, инициирующий начало работы """
        self._working_in_subthreads = True
        self._setup()

        # Создадим и запустим потоки, в которых будет выполняться логика работы
        self._executors.append(
            Thread(target=self._checking_command_queue, args=(), daemon=True)
        )
        for thread in self._executors:
            thread.start()

    @abstractmethod
    def _setup(self):
        """ Метод запуска выполнения работника """
        pass

    def new_message(self, message: Message):
        """ Добавление нового сообщения в очередь сообщений в основной процесс """
        self._message_queue.put(message)

    def _checking_command_queue(self):
        """ Постоянная проверка очереди поступивших команд """
        while self._working_in_subthreads:
            if not self._command_queue.empty():
                try:
                    command = str(self._command_queue.get())
                    self._command_handler(command)
                except ValueError:
                    pass

    def _command_handler(self, command_name: str, *args, **kwargs):
        """ Метод для обработки поступивших команд """

        # TODO: при успешном приёме команды необходимо в очередь сообщений отправить
        #       подтверждение получения и статус выполнения, которые будут отслеживаться
        #       менеджером в основном процессе программы.

        if hasattr(self, command_name) and callable(getattr(self, command_name)):
            method = getattr(self, command_name)
            return method(*args, **kwargs)
        else:
            raise ValueError(f"Unknown command: {command_name}")

