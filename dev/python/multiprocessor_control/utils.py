# System imports
from typing import Type, Callable
from threading import Thread
import signal

# External imports
from multiprocessing import Process, Queue as ProcessQueue

# User imports
from .multiprocessing_worker import MultiprocessingWorker

##########################################################

def run_in_new_process(func: Callable, *args, **kwargs) -> Process:
    """ Функция для выполнения функции func в новом процессе """
    process = Process(target=func, args=args, kwargs=kwargs, daemon=True)
    process.start()
    return process

def run_mlt_worker(mlt_worker_type: Type[MultiprocessingWorker],
                   command_queue: ProcessQueue,
                   message_queue: ProcessQueue):
    """
    Создание объекта работника и его запуск с заданными каналами связи
    :param mlt_worker_type: тип работника
    :param command_queue: очередь для команд к работнику
    :param message_queue: очередь сообщений от работника
    """

    # Если функция запущена в другом процессе, то необходимо корректно завершить данный процесс
    # Тк mlt_worker_type должен быть завершён из основного процесса, то подключим сигналы к пустой lambda функции
    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, lambda signum, frame: ...)

    worker = mlt_worker_type(command_queue, message_queue)
    thread = Thread(target=worker.start, args=(), daemon=True)

    # Запустим поток и будем ждать его завершение
    thread.start()
    thread.join()

