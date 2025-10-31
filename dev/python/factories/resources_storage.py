# System imports
from abc import ABC, abstractmethod
from threading import Thread
from pprint import pformat

# External imports

# User imports
from utils import singleton, AppLogger

##########################################################

class Resource(ABC):
    name: str

    def __init__(self, resource_name: str):
        self.name = resource_name

    @abstractmethod
    def cleanup(self):
        """ Явный метод отчистки """
        pass

    @abstractmethod
    def setup(self):
        """ Конфигурация ресурса """
        pass

    @abstractmethod
    def start(self):
        """ Запуск ресурса """
        pass

    @abstractmethod
    def commands_executor(self, command_name: str, *args, **kwargs):
        """
        Функция для выполнения поступившей команды.
        Данный метод вызывается напрямую из основного потока.
        """
        pass

# --------------------------------------

@singleton
class ResourcesStorage:
    """
    Класс, в котором будем хранить все ресурсы, созданные
    в основном процессе работы программы
    """
    def __init__(self):
        super().__init__()
        self._resources: dict[str, Resource] = {}
        self._threads: list[Thread] = []
        self._app_logger: AppLogger = AppLogger()

    def get_resource(self, name: str) -> Resource:
        if name in self._resources.keys():
            resource = self._resources[name]
            self._app_logger.debug(f'\n{self.__class__.__name__}:\tResource requested {resource} with name {resource.name}')
            return resource
        else:
            self._app_logger.exception(f'\n{self.__class__.__name__}:\tResource "{name}" not found')
            raise KeyError(f'Resource "{name}" not found')

    def add_resource(self, resource: Resource):
        """
        Добавление ресурса в словарь, содержащий все остальные ресурсы
        """
        self._app_logger.debug(f'\n{self.__class__.__name__}:\tAdded resource {resource} with name {resource.name}')
        self._resources[resource.name] = resource

    def cleanup_all(self):
        """
        Явный вызов методов cleanup у всех сохранённых ресурсов
        """
        # -----------------------
        self._app_logger.info(f'\nCall the method {self.__class__.__name__}.cleanup_all()')
        # -----------------------

        for resource in self._resources.values():
            self._app_logger.debug(f'\n{self.__class__.__name__}:\tCall the method {resource}.cleanup()')
            resource.cleanup()

        for thread in self._threads:
            self._app_logger.debug(f'\n{self.__class__.__name__}:\tJoining thread {thread}')
            thread.join()

        # -----------------------
        self._app_logger.info(f'\n{self.__class__.__name__}.cleanup_all() is completed')
        # -----------------------

    def setup_all(self):
        """
        Явный метод конфигурирования всех ресурсов
        """
        # -----------------------
        self._app_logger.info(f'\nCall the method {self.__class__.__name__}.setup_all()')
        # -----------------------

        for resource in self._resources.values():
            self._app_logger.debug(f'\nCall the method {resource}.setup()')
            resource.setup()

        # -----------------------
        self._app_logger.info(f'\n{self.__class__.__name__}.setup_all() is completed')
        # -----------------------

    def start_all(self):
        """
        Метод для запуска метода start() у всех ресурсов в новых потоках
        """
        # -----------------------
        self._app_logger.info(f'\nCall the method {self.__class__.__name__}.start_all()')
        # -----------------------

        for resource in self._resources.values():
            thread = Thread(target=resource.start, args=(), daemon=True)
            self._threads.append(thread)
            thread.start()
            self._app_logger.debug(f'\nCall {resource}.start() in {thread}')

        # -----------------------
        self._app_logger.info(f'\n{self.__class__.__name__}.start_all() is completed')
        # -----------------------

    def __str__(self):
        return pformat(self._resources)
