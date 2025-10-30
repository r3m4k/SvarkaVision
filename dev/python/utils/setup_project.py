# System imports
import sys
import signal
import os
from time import sleep

# External imports

# User imports
from consts import Mode, signals, debug_dir
from factories import ResourcesStorage, PhotoReceiverManagerFactory
from messages_to_main_checker import MessagesToMainChecker
from .end_of_program import enf_of_program

##########################################################


def setup_project():
    """
    Настройка проекта
    """

    if not os.path.exists(debug_dir):
        os.mkdir(debug_dir)

    resource_storage = ResourcesStorage()

    # Подключим обработку завершающих сигналов
    for sig in signals.keys():
        signal.signal(sig, enf_of_program)

    # Инициализируем источник фотографий
    PhotoReceiverManagerFactory().create_resource()

    # Инициализируем проверку сообщений
    # ВАЖНО инициализировать проверку сообщений в самом конце, для отработки всех сообщений при завершении программы
    MessagesToMainChecker()

    # Запустим все ресурсы
    resource_storage.setup_all()
    resource_storage.start_all()