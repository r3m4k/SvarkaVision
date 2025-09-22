# System imports
import json
from pprint import pprint
from queue import Empty

# External imports

# User imports
from consts import Mode, SETTINGS_FILE
from settings_manager import SettingsManager
from PhotoReceiving import PhotoSource
from CommunationInterfaces import run_report_sender

##########################################################

def setup_project():
    """
    Создание и запуск всех процессов
    """
    pass

def test():
    """
    Запуск тестов
    """
    # Загрузка параметров в settings.json
    with open(SETTINGS_FILE, 'r') as settings_file:
        settings = json.load(settings_file)

    settings['Mode'] = Mode.RELEASE
    with open(f'{SETTINGS_FILE}', 'w') as settings_file:
        json.dump(settings, settings_file)


def main():
    """
    Запуск всего проекта
    """

    print('Запуск проекта')

    settings_manager = SettingsManager()
    settings_manager.update_setting('Mode', Mode.DEBUG)
    settings_manager.save_settings()

    pprint(settings_manager.settings)
    print()

    photo_source = PhotoSource()
    try:
        while True:
            print(photo_source.get_photo())

    except Empty:
        print('\nEnd of photo queue\n')

    run_report_sender()

    photo_source.cleanup()


# --------------------------------------

if __name__ == "__main__":
    main()