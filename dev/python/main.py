# System imports
import sys
import signal
import os
from time import sleep

# External imports

# User imports
from consts import Mode, signals, debug_dir
from factories import ResourcesStorage
from factories import PhotoReceiverManagerFactory
from utils import MessagesToMain, SettingsManager
from messages_to_main_checker import MessagesToMainChecker


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

    # Инициализируем проверку сообщений в основной поток
    # ВАЖНО инициализировать проверку сообщений в самом конце, для отработки всех сообщений
    MessagesToMainChecker()

    # Запустим все ресурсы
    resource_storage.setup_all()


def test():
    """
    Запуск тестов
    """
    pass


def main():
    """
    Запуск всего проекта
    """
    print('Запуск проекта')

    settings_manager = SettingsManager()
    settings_manager.update_setting('Mode', Mode.DEBUG)
    settings_manager.save_settings()

    setup_project()

    while True:
        sleep(1)


def enf_of_program(signum, frame):
    resource_storage = ResourcesStorage()

    print(f'Получен сигнал {signals[signum]}')
    resource_storage.cleanup_all()

    print(f'ResourcesStorage:\n'
          f'{resource_storage}')
    print(f'MessagesToMain().qsize(): {MessagesToMain().qsize()}')

    sys.exit(0)

# --------------------------------------

if __name__ == "__main__":
    main()