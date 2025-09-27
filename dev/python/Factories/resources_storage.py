# System imports
from abc import ABC, abstractmethod
from typing import Dict
from pprint import pformat

# External imports

# User imports
from singleton import Singleton

##########################################################

class Resource(ABC):
    name: str

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def cleanup(self):
        """ Явный метод отчистки """
        pass

# --------------------------------------

class ResourcesStorage(Singleton):
    """
    Класс, в котором будем хранить все ресурсы, созданные
    в основном процессе работы программы
    """
    def __init__(self):
        if not getattr(self, '_initialized', False):
            super().__init__()
            self._resources: Dict[str, Resource] = {}

    def get_resource(self, name: str) -> Resource:
        if name in self._resources.keys():
            return self._resources[name]
        else:
            raise KeyError(f"Resource '{name}' not found")

    def add_resource(self, resource: Resource):
        self._resources[resource.name] = resource

    def cleanup(self):
        """
        Явный вызов методов cleanup у всех сохранённых ресурсов
        """
        for resource in self._resources.values():
            resource.cleanup()

    def __str__(self):
        return pformat(self._resources)
