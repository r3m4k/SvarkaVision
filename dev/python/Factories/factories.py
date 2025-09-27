# System imports
from abc import ABC, abstractmethod

# External imports

# User imports
from .resources_storage import Resource, ResourcesStorage
from PhotoReceiving import PhotoReceiverManager

##########################################################

class BaseFactory(ABC):
    """
    Базовый класс для фабрик ресурсов, которые могут быть
    использованы в данном проекте
    """
    @abstractmethod
    def create_resource(self, resource_name: str) -> Resource:
        """ Абстрактный метод для создания ресурса """
        pass

    @staticmethod
    def _register_resource(resource: Resource):
        """ Метод для добавления ресурса в ResourceStorage """
        resource_storage = ResourcesStorage()
        resource_storage.add_resource(resource)

# --------------------------------------

class PhotoReceiverManagerFactory(BaseFactory):
    """ Фабрика менеджеров для приёмника фотографий """
    def create_resource(self, resource_name: str = 'photo_receiver_manager') -> Resource:
        """ Создание PhotoReceiverManager """
        resource = PhotoReceiverManager(resource_name=resource_name)
        self._register_resource(resource)
        return resource