# System imports
from abc import abstractmethod
import asyncio
from multiprocessing import Queue as ProcessQueue
from threading import Thread, current_thread
from typing import Callable

# External imports

# User imports
from messages import Message, MessageMode
from consts import signals
from utils import Logger

##########################################################

class MultiprocessingWorker:
    """
    Базовый класс, для создания объекта, который будет выполняться
    в отдельном процессе и поддерживающий двустороннюю коммуникацию
    с основным процессом через очереди команд и сообщений.

    Также автоматически выполняет очистку ресурсов при удалении объекта.
    """

    def __init__(self, command_queue: ProcessQueue, message_queue: ProcessQueue):
        self._loop = asyncio.new_event_loop()   # Основной планировщик задач работника
        self._tasks: list[asyncio.Task] = []    # Список задач, которые запустятся при self.start
        asyncio.set_event_loop(self._loop)

        self._command_queue = command_queue     # Очередь поступивших команд из основного процесса
        self._message_queue = message_queue     # Очередь для отправки сообщений в основной процесс

        # Необходимые флаги
        self._cleanup_done_flag: bool = False
        self._running_flag: bool = False

        # Дополнительные ресурсы
        self._logger: Logger = None
        self._command_handlers: dict[str, Callable[[], None]] = {
            'cleanup': self.cleanup,
            'echo': lambda: self._message_queue.put(f'{self.__class__.__name__} -> echo')
        }

    def __del__(self):
        if not self._cleanup_done_flag:
            self.cleanup()

    # --------------------------------
    # Основные методы базового класса
    # --------------------------------

    def cleanup(self):
        """ Явный метод отчистки """
        self._running_flag = False
        self._logger.debug('Doing cleanup')

        try:
            self._loop.call_soon_threadsafe(self._loop.stop)
        except RuntimeError:    #   RuntimeError('Event loop is closed')
            pass

        self._logger.debug(f'{self.__class__.__name__}: cleanup done')

    def start(self):
        """ Метод, инициирующий начало работы """
        self._running_flag = True
        self.setup()

        self._tasks.append(self._loop.create_task(self._checking_command_queue()))

        # Запустим планировщик
        try:
            self._loop.run_forever()

        # Отработаем остановку выполнения задач после вызова self._cleanup
        finally:
            for task in self._tasks:
                self._logger.debug(f'Canceling task {task}')
                task.cancel()

            self._loop.run_until_complete(asyncio.gather(*self._tasks, return_exceptions=True))
            self._loop.close()
            self._logger.debug(f'{self._loop} stopped')
            self._new_message(Message(MessageMode.LogInfo,
                                      f'{self.__class__.__name__} stopped'))

    @abstractmethod
    def setup(self):
        """ Абстрактный метод конфигурации работника """
        pass

    # --------------------------------
    # Собственные методы класса
    # --------------------------------

    def _new_message(self, message: Message):
        """ Добавление нового сообщения в очередь сообщений в основной процесс """
        self._message_queue.put(message)
        self._logger.debug(message=f'\n{message.to_format_string()}')

    async def _checking_command_queue(self):
        """ Метод для проверки очереди поступивших команд """
        while self._running_flag:
            if not self._command_queue.empty():
                command: str = self._command_queue.get()
                self._logger.debug(f'New command: {command}')
                self._input_command_handler(command)

            await asyncio.sleep(0.5)

    def _input_command_handler(self, command: str):
        """ Метод вызова нужного обработчика поступившей команды """
        try:
            command_handler = self._command_handlers[command]
            command_handler()
        except KeyError:
            self._new_message(Message(MessageMode.LogInfo, f'Unknown command {command}'))
