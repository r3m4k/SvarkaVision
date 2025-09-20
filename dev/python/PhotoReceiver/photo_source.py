# System imports
import json
from importlib.metadata import files
from queue import Queue
from typing import Any
from pathlib import Path

# External imports

# User imports
from settings_manager import SettingsManager
from consts import Mode

##########################################################

class SourceStatus:
    """
    Класс для хранения состояния источника фотографий
    """
    # Общие состояния
    Initialized = 'Initialized'
    Active = 'Active'
    Stopped = 'Stopped'

    # Конкретные состояния, описывающие причину остановки
    EndOfDataset = 'EndOfDataset'
    DatasetNotFounded = 'DatasetNotFounded'
    Disconnected = 'Disconnected'

# --------------------------------------


class PhotoSource:
    """
    Класс для получения фотографий с камеры или с готового датасета
    """

    def __init__(self):
        self._source: str = None
        self._source_params: dict[str, Any]
        self._photo_queue: Queue[str] = Queue()

        # Статус, который будем менять в зависимости от состояния класса
        self.status: str = SourceStatus.Initialized

        self._setup()

    def _setup(self):
        """
        Полная настройка источника фотографий
        """
        settings_manager = SettingsManager()
        match settings_manager.settings['Mode']:
            case Mode.RELEASE:
                self._source = 'camera'
            case Mode.DEBUG:
                self._source = 'local_dir'
            case Mode.TEST:
                self._source = 'local_dir'
            case _:
                pass
        self._source_params = settings_manager.settings['PhotoReceiver']['sources_params']
        self.status = SourceStatus.Active

        # Загрузим одну фотографию в очередь
        self._load_photo(1)

    def get_photo(self) -> str:
        """
        Получение пути к фотографии из очереди
        """
        self._load_photo()
        return self._photo_queue.get(timeout=1)

    def _load_photo(self, num=1):
        """
        Загрузка num фотографии в очередь из источника.
        """
        if self._source == 'camera':
            self._load_photo_from_camera(num)
        elif self._source == 'local_dir':
            self._load_photo_from_dataset(num)

    def _load_photo_from_dataset(self, num):
        """
        Загрузка фотографии в очередь из датасета
        """
        # Если фотографии загружаются с датасета, то при первом запуске единожды добавим их все в очередь _photo_queue
        if self.status == SourceStatus.Active:
            _label = 'weld_'     # Часть названия файлов с фотографиями сварки, которая используется для их идентификации
            _dir_path = Path(self._source_params['local_dir']['path'])
            try:
                if not _dir_path.exists():
                    raise FileExistsError
                _photo_names_list = [item for item in _dir_path.iterdir() if item.is_file() and _label in item.name]
                for _photo in _photo_names_list:
                    self._photo_queue.put(str(_photo))

            except KeyError:
                self.status = SourceStatus.DatasetNotFounded
                raise RuntimeError(
                    'Bad settings for photo source!\n'
                    'Tried to get settings["local_dir"]["path"], but the KeyError was raised.'
                )
            except FileExistsError:
                self.status = SourceStatus.DatasetNotFounded
                raise RuntimeError(
                    f'Directory {_dir_path} does\'t exist.\n'
                    f'Unable to load photos from dataset.'
                )
            self.status = SourceStatus.EndOfDataset

        elif self.status == SourceStatus.EndOfDataset:
            pass

        else:
            raise RuntimeError(f'Unsupported status {self.status} for loading photos from dataset.')

    def _load_photo_from_camera(self, num):
        """
        Загрузка фотографии в очередь из подключённой камеры
        """
        pass