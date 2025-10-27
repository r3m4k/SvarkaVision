# System imports

# External imports

# User imports
from consts import Mode
from utils import SettingsManager, setup_project

##########################################################

def test():
    """
    Запуск тестов
    """
    pass

# --------------------------------------

def main():
    """
    Запуск проекта
    """
    settings_manager = SettingsManager()
    settings_manager.update_setting('Mode', Mode.DEBUG)
    settings_manager.save_settings()

    setup_project()

    while True:
        continue

# --------------------------------------

if __name__ == "__main__":
    main()