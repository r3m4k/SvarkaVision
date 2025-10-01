# System imports
from queue import Queue

# External imports

# User imports
from singleton import Singleton

##########################################################

class MessagesToMain(Singleton):
    """
    Класс, реализующий одиночную очередь сообщений основному потоку.
    Должен использоваться исключительно в рамках одного процесса!
    """
    def __init__(self):
        super().__init__()
        self._messages_queue: Queue[str] = Queue()

    def put(self, message: str):
        """ Добавление элемента в очередь """
        self._messages_queue.put(message)

    def get(self) -> str:
        """ Получение элемента из очереди """
        return self._messages_queue.get()