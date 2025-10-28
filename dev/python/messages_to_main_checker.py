# System imports
from queue import Queue
from threading import Thread

# External imports

# User imports
from utils import MessagesToMain
from messages import Message
from factories import Resource, ResourcesStorage

##########################################################

class MessagesToMainChecker(Resource):
    """
    Класс для постоянной проверки сообщений в MessagesToMain
    в дочернем потоке
    """
    def __init__(self):
        super().__init__('messages_to_main_checker')
        self._messages_to_main = MessagesToMain()
        self._working_in_subthreads: bool = True

        # Поток, в котором запустим проверку очереди сообщений
        self._executor_thread: Thread = Thread(
            target=self._infinite_checking, args=(), daemon=True
        )

        # Добавим MessagesToMainChecker (себя же) в список ресурсов
        ResourcesStorage().add_resource(self)

    def cleanup(self):
        self._working_in_subthreads = False
        self._executor_thread.join()

    def setup(self):
        self._executor_thread.start()

    def start(self):
        pass

    def commands_executor(self, command_name: str, *args, **kwargs):
        return

    def _infinite_checking(self):
        """
        Функция для постоянного вывода сообщений
        """
        while self._working_in_subthreads:
            if not self._messages_to_main.empty():
                message = self._messages_to_main.get()
                print(message.to_format_string())
