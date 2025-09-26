# System imports
from multiprocessing import Queue as ProcessQueue

# External imports

# User imports

##########################################################

class MultiprocessingWorker:
    """
    Базовый класс, для создания объекта, который будет выполняться
    в отдельном процессе и поддерживающий двустороннюю коммуникацию
    с основным процессом через очереди команд и сообщений.

    Также автоматически выполняет очистку ресурсов при удалении объекта.
    """

    def __init__(self, command_queue: ProcessQueue[str], message_queue: ProcessQueue[str], ):
        self._command_queue = command_queue     # Очередь поступивших команд из основного процесса
        self._message_queue = message_queue     # Очередь для отправки сообщений в основной процесс

        # Необходимые флаги
        self._cleanup_done_flag = False

    def __del__(self):
        if not self._cleanup_done_flag:
            self.cleanup()

    def cleanup(self):
        """ Явный метод отчистки """
        pass

    def _setup(self):
        """ Метод запуска выполнения работника """
        pass

    def _command_handler(self, command_name, *args, **kwargs):
        """ Метод для обработки поступивших команд """

        # TODO: при успешном приёме команды необходимо в очередь сообщений отправить
        #       подтверждение получения и статус выполнения, которые будут отслеживаться
        #       менеджером в основном процессе программы.

        if hasattr(self, command_name) and callable(getattr(self, command_name)):
            method = getattr(self, command_name)
            return method(*args, **kwargs)
        else:
            raise ValueError(f"Unknown command: {command_name}")