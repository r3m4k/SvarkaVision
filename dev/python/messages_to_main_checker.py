# System imports
from queue import Queue
from threading import Thread

# External imports

# User imports
from utils import MessagesToMain, AppLogger
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
        self._app_logger: AppLogger = AppLogger()

        # Поток, в котором запустим проверку очереди сообщений
        self._executor_thread: Thread = Thread(
            target=self._infinite_checking, args=(), daemon=True
        )

        # Добавим MessagesToMainChecker (себя же) в список ресурсов
        ResourcesStorage().add_resource(self)

        self._cleanup_done = False

    def __del__(self):
        if not self._cleanup_done:
            self.cleanup()

    def cleanup(self):
        """ Явный метод для завершения работы """
        self._working_in_subthreads = False
        self._app_logger.debug(f'\n{self.__class__.__name__}:\tJoining {self._executor_thread}')
        self._executor_thread.join()
        self._app_logger.debug(f'{self.__class__.__name__} info:\n'
                               f'{self._info()}')
        self._cleanup_done = True

    def setup(self):
        pass

    def start(self):
        self._executor_thread.start()

    def commands_executor(self, command_name: str, *args, **kwargs):
        pass

    def _infinite_checking(self):
        """
        Постоянная обработка поступивших сообщений
        """
        while self._working_in_subthreads or not self._messages_to_main.empty():
            if not self._messages_to_main.empty():
                message = self._messages_to_main.get()
                print(message.to_format_string())

    def _info(self):
        return (f'messages_to_main: {self._messages_to_main} // qsize = {self._messages_to_main.qsize()}\n'
                f'executor_thread: {self._executor_thread}')