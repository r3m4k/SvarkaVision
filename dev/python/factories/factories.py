# System imports
from abc import ABC
from typing import Type

# External imports

# User imports
from .resources_storage import Resource, ResourcesStorage

##########################################################

class BaseFactory(ABC):
    """
    Базовый класс для фабрик ресурсов, которые могут быть
    использованы в данном проекте
    """
    resource = None

    def create_resource(self, resource_name: str = 'resource', **kwargs) -> Resource:
        """ Метод для создания ресурса """
        if self.resource is not None:
            self._register_resource(self.resource)
            return self.resource
        else:
            raise RuntimeError('self.resource is None')

    @staticmethod
    def _register_resource(resource: Resource):
        """ Метод для добавления ресурса в ResourceStorage """
        ResourcesStorage().add_resource(resource)

# --------------------------------------

from photo_receiving import PhotoReceiverManager

class PhotoReceiverManagerFactory(BaseFactory):
    def create_resource(self, resource_name: str = 'photo_receiver_manager', **kwargs) -> Resource:
        """ Создание PhotoReceiverManager """
        self.resource = PhotoReceiverManager(resource_name=resource_name)
        return super().create_resource()
