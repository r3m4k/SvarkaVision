# System imports
from threading import Thread
from time import sleep
from typing import Type

from multiprocessing import Process, Queue as ProcessQueue

# External imports

# User imports
from factories import Resource
from utils import MessagesToMain
from .multiprocessing_worker import MultiprocessingWorker
from .utils import run_in_new_process, run_mlt_worker
from messages import MessageMode, Message

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

        self._worker_process = Process()        # Процесс, в котором будет запущен работник
        self._executors: list[Thread] = []      # Список потоков, в которых запущены дополнительные задачи

        self._commands_to_worker: ProcessQueue = ProcessQueue()         # Очередь для отправки команд работнику
        self._messages_from_worker: ProcessQueue = ProcessQueue()       # Очередь поступивших сообщений от работника

        # Необходимые флаги
        self._cleanup_done: bool = False
        self._working_in_subthreads: bool = False

    def __del__(self):
        if not self._cleanup_done:
            self.cleanup()

    # -------------------------------------------
    # Реализация наследуемых методов
    # -------------------------------------------

    def setup(self):
        # Настроим self._worker для запуска работника в новом процессе
        self._worker_process = Process(target=run_mlt_worker,
                                       args=(self._worker, self._commands_to_worker, self._messages_from_worker),
                                       daemon=True)

        # Запустим проверку сообщений от работника в новом потоке
        self._executors.append(
            Thread(target=self._checking_messages_from_worker, args=(), daemon=True)
        )

    def start(self):
        """ Метод для запуска всех потоков и процессов """
        self._working_in_subthreads = True

        self._worker_process.start()
        for thread in self._executors:
            thread.start()

    def cleanup(self):
        """ Явный метод отчистки использованных ресурсов """
        self._cleanup_done= True
        self._working_in_subthreads = False

        # Завершим работу дочернего процесса, в котором запущен работник
        self._commands_to_worker.put('cleanup')
        self._worker_process.join()

        # Завершим работу всех дочерних процессов
        for thread in self._executors:
            thread.join()

    def commands_executor(self, command_name: str, *args, **kwargs):
        """ Обработка поступившей команды """
        pass

    # -------------------------------------------
    # Реализация собственных методов
    # -------------------------------------------

    def _checking_messages_from_worker(self):
        while self._working_in_subthreads:
            if not self._messages_from_worker.empty():

                # Прочитаем сообщение из очереди
                message: Message = self._messages_from_worker.get()

                match message.mode:
                    case MessageMode.LogInfo:
                        self._messages_to_main.put(message)

                    case MessageMode.Command:
                        pass
