# System imports
import json
from pathlib import Path
from typing import Any, Dict, cast, Literal

# External imports

# User imports
from consts import SETTINGS_FILE, DEFAULT_SETTINGS, Mode, LogLevel
from configs import AppConfig, AppConfigKeys

##########################################################

class SettingsManager:
    def __init__(self):
        self._settings_file = Path(SETTINGS_FILE)
        self.settings: AppConfig = self._load_settings()

        # Параметры, которые могут быть изменены во время работы программы
        self._dynamic_settings: list[AppConfigKeys] = [
            AppConfigKeys.Mode,
            AppConfigKeys.LogLevel
        ]

    def _load_settings(self) -> AppConfig:
        """ Загрузка настроек с обработкой ошибок """
        if not self._settings_file.exists():
            return self._get_default_settings()

        try:
            return json.loads(self._settings_file.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            print(f"Ошибка JSON, используются настройки по умолчанию: {e}")
            return self._get_default_settings()

    @staticmethod
    def _get_default_settings() -> AppConfig:
        """ Настройки по умолчанию """
        return DEFAULT_SETTINGS

    def update_setting(self, key: str, value: Any) -> None:
        """Обновление конкретной настройки с проверкой"""

        try:
            if key not in set(AppConfig.__required_keys__):
                raise KeyError()

            typed_key: AppConfigKeys = AppConfigKeys.from_string(key)
            if key in self._dynamic_settings:
                self.settings[typed_key] = value
            else:
                raise KeyError()

        except KeyError:
            raise KeyError('An attempt to change an immutable or non-existent setting\n')

    def save_settings(self) -> None:
        """ Сохранение настроек с форматированием """
        try:
            self._settings_file.write_text(
                json.dumps(self.settings, indent=4, ensure_ascii=False),
                encoding='utf-8'
            )
        except IOError as e:
            print(f"Ошибка сохранения настроек: {e}")
            raise