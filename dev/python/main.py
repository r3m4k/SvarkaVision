# System imports
import sys
import json
from pprint import pprint
from queue import Empty
import signal

# External imports

# User imports
from consts import Mode, SETTINGS_FILE
from settings_manager import SettingsManager
# from photo_receiving import PhotoSource
from communication_interfaces import run_report_sender
from factories import ResourcesStorage
from factories import PhotoReceiverManagerFactory


##########################################################

def setup_project():
    """
    Настройка проекта
    """
    print(f'ResourcesStorage:\n'
          f'{ResourcesStorage()}')
    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, enf_of_program)

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

    setup_project()

    settings_manager = SettingsManager()
    settings_manager.update_setting('Mode', Mode.DEBUG)
    settings_manager.save_settings()

    pprint(settings_manager.settings)
    print()

    # run_report_sender()
    PhotoReceiverManagerFactory().create_resource()

    print('Программа выполнила все действия.\n'
          'Ожидание завершения работы пользователем')
    while True:
        continue


def enf_of_program(signum, frame):
    signals = {'2': 'signal.SIGINT', '15': 'signal.SIGTERM'}
    print(f'Получен сигнал {signals[str(signum)]}')

    print(f'ResourcesStorage:\n'
          f'{ResourcesStorage()}')
    ResourcesStorage().cleanup_all()

    sys.exit(0)

# --------------------------------------

if __name__ == "__main__":
    main()