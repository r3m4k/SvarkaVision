# System imports
import json
from pathlib import Path
from typing import Any, Dict

# External imports

# User imports
from consts import SETTINGS_FILE, Mode, LogLevel
from configs import AppConfig

##########################################################

class SettingsManager:
    def __init__(self):
        self._settings_file = Path(SETTINGS_FILE)
        self.settings: AppConfig = self._load_settings()

        # Параметры, которые могут быть изменены во время работы программы
        self._dynamic_settings = ["Mode", "LogLevel"]

    def _load_settings(self) -> AppConfig:
        """Загрузка настроек с обработкой ошибок"""
        if not self._settings_file.exists():
            return self._get_default_settings()

        try:
            return json.loads(self._settings_file.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            print(f"Ошибка JSON, используются настройки по умолчанию: {e}")
            return self._get_default_settings()

    @staticmethod
    def _get_default_settings() -> AppConfig:
        """Настройки по умолчанию"""
        return {
            "Mode": Mode.DEBUG,
            "LogLevel": LogLevel.INFO,
            "PhotoReceiver": {
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

    def update_setting(self, key: str, value: Any) -> None:
        """Обновление конкретной настройки с проверкой"""
        if key in self._dynamic_settings and key in self.settings.keys():
            self.settings[key] = value
        else:
            raise KeyError('An attempt to change an immutable or non-existent setting\n')

    def save_settings(self) -> None:
        """Сохранение настроек с форматированием"""
        try:
            self._settings_file.write_text(
                json.dumps(self.settings, indent=4, ensure_ascii=False),
                encoding='utf-8'
            )
        except IOError as e:
            print(f"Ошибка сохранения настроек: {e}")
            raise