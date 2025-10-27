# System imports
from queue import Queue
from threading import Thread

# External imports

# User imports
from utils import singleton
from messages import Message

##########################################################

@singleton
class MessagesToMain:
    """
    Класс, реализующий одиночную очередь сообщений основному потоку.
    Должен использоваться исключительно в рамках одного процесса!
    """
    def __init__(self):
        super().__init__()
        self._messages_queue: Queue[Message] = Queue()

    def put(self, message: Message):
        """ Добавление элемента в очередь """
        self._messages_queue.put(message)

    def empty(self) -> bool:
        return self._messages_queue.empty()

    def get(self) -> Message:
        """ Получение элемента из очереди """
        return self._messages_queue.get()

    def qsize(self) -> int:
        return self._messages_queue.qsize()
