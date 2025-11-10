# System imports
from enum import Enum
from typing import Any
from time import sleep
from threading import Thread
from pathlib import Path
from queue import Queue

# External imports

# User imports
from utils import SettingsManager
from consts import Mode

##########################################################

class SourceStatus(Enum):
    """
    Класс для хранения состояния источника фотографий
    """
    # Общие состояния
    Initialized = 'Initialized'
    Active = 'Active'
    Stopped = 'Stopped'
    CleanedUp = 'CleanedUp'

    # Конкретные состояния, описывающие причину остановки
    EndOfDataset = 'EndOfDataset'
    DatasetNotFounded = 'DatasetNotFounded'
    Disconnected = 'Disconnected'

# --------------------------------------

class PhotoProcessingStage(Enum):
    """
    Стадии обработки фотографии в приложении
    """
    AWAITING_PHOTO = 0      # Ожидание новой фотографии
    PHOTO_LOADED = 1        # Фотография загружена

# --------------------------------------

class PhotoSource:
    """
    Класс для получения фотографий с камеры или с готового датасета
    """

    def __init__(self):
        self._source: str = ''
        self._source_params: dict[str, Any]
        self._photo_queue: Queue[str] = Queue()
        self._loading_thread: Thread = Thread()
        self._loading_flag = False

        # Статус, который будем менять в зависимости от состояния источника
        self._source_status: SourceStatus = SourceStatus.Initialized

        # Текущая стадия обработки фотографии
        self._current_stage: PhotoProcessingStage = PhotoProcessingStage.AWAITING_PHOTO

        self._setup()

    def __del__(self):
        if self._source_status is not SourceStatus.CleanedUp:
            self.cleanup()

    def cleanup(self):
        """
        Явный метод отчистки использованных ресурсов
        """
        # print('cleanup')
        self._source_status = SourceStatus.CleanedUp
        self._loading_flag = False
        sleep(0.1)
        self._loading_thread.join()

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
        self._source_params = settings_manager.settings['PhotoReceiving']['sources_params']
        self._source_status = SourceStatus.Active
        self._loading_thread = Thread(target=self._infinite_loading_photo, args=(), daemon=True)

        # Начнём загрузку фотографий в очередь
        self._loading_flag = True
        self._loading_thread.start()

    def get_photo(self) -> str:
        """
        Получение пути к фотографии из очереди
        """
        self._current_stage = PhotoProcessingStage.AWAITING_PHOTO
        return self._photo_queue.get(timeout=1)

    def _infinite_loading_photo(self):
        """
        Постоянный вызов загрузки фотографий в очередь
        """
        while self._loading_flag:
            if self._current_stage == PhotoProcessingStage.AWAITING_PHOTO:
                self._load_photo()
            elif self._current_stage == PhotoProcessingStage.PHOTO_LOADED:
                sleep(0.5)

    def _load_photo(self):
        """
        Загрузка фотографии в очередь из источника.
        """
        if self._source == 'camera':
            self._load_photo_from_camera()
        elif self._source == 'local_dir':
            self._load_photo_from_dataset()
        self._current_stage = PhotoProcessingStage.PHOTO_LOADED

    def _load_photo_from_dataset(self):
        """
        Загрузка фотографии в очередь из датасета
        """
        # Если фотографии загружаются с датасета, то при первом запуске сразу добавим их все в очередь _photo_queue
        if self._source_status == SourceStatus.Active:
            _label = 'weld_'     # Часть названия файлов с фотографиями сварки, которая используется для их идентификации
            _dir_path = Path(self._source_params['local_dir']['path'])
            try:
                if not _dir_path.exists():
                    raise FileExistsError

                _photo_names_list = [item for item in _dir_path.iterdir() if item.is_file() and _label in item.name]
                for _photo in _photo_names_list:
                    self._photo_queue.put(str(_photo))

            except KeyError:
                self._source_status = SourceStatus.DatasetNotFounded
                raise RuntimeError(
                    'Bad settings for photo source!\n'
                    'Tried to get settings["local_dir"]["path"], but the KeyError was raised.'
                )
            except FileExistsError:
                self._source_status = SourceStatus.DatasetNotFounded
                raise RuntimeError(
                    f'Directory {_dir_path} does\'t exist.\n'
                    f'Unable to load photos from dataset.'
                )
            self._source_status = SourceStatus.EndOfDataset

        elif self._source_status == SourceStatus.EndOfDataset:
            pass

        else:
            raise RuntimeError(f'Unsupported status {self._source_status} for loading photos from the dataset.')

    def _load_photo_from_camera(self):
        """
        Загрузка фотографии в очередь из подключённой камеры
        """
        pass
