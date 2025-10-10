# System imports
from typing import Type, Callable

# External imports
from multiprocessing import Process, Queue

# User imports
from .multiprocessing_worker import MultiprocessingWorker

##########################################################

def run_in_new_process(func: Callable, *args, **kwargs) -> Process:
    """ Функция для выполнения функции func в новом процессе """
    process = Process(target=func, args=args, kwargs=kwargs, daemon=True)
    process.start()
    return process

def run_mlt_worker(mlt_worker_type: Type[MultiprocessingWorker],
                   command_queue: Queue,
                   message_queue: Queue):
    """
    Создание объекта работника и его запуск с заданными каналами связи
    :param mlt_worker_type: тип работника
    :param command_queue: очередь для команд к работнику
    :param message_queue: очередь сообщений от работника
    """
    worker = mlt_worker_type(command_queue, message_queue)
    worker.start()
