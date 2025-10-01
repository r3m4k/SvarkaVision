# Файл для хранения константных значений

# --------------------------------------

class Mode:
    DEBUG = "debug"
    RELEASE = "release"
    TEST = "test"

# --------------------------------------

class LogLevel:
    DEBUG = "Debug"
    INFO = "Info"

# --------------------------------------

# Относительный путь к json файлу с настройками
SETTINGS_FILE = './settings.json'

# --------------------------------------

# Путь к датасету со сварочными швами
DATASET_DIR = './WeldDataset'

# --------------------------------------

from configs import AppConfig

DEFAULT_SETTINGS: AppConfig = {
            "Mode": Mode.DEBUG,
            "LogLevel": LogLevel.INFO,
            "photo_receiving": {
                "host": "localhost",
                "port": 5050,
                "sources_params": {
                    "camera": {},
                    "local_dir": {
                        "path": "./WeldDataset"
                    }
                }
            },
            "QualityController": {},
            "ReportSender": {
                "host": "localhost",
                "port": 5005
            }
        }

# --------------------------------------