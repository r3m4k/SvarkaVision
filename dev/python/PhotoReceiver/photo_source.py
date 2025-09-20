# System imports
import json
from queue import Queue

# External imports

# User imports
from consts import SETTINGS_FILE

##########################################################

class PhotoSource:
    """
    Класс для получения фотографий с камеры или с готового датасета
    """

    def __init__(self):
        self._source: str = None
        self._photo_queue: Queue[str] = Queue()

    def _setup(self):
        """
        Полная настройка источника фотографий
        """
        with open(SETTINGS_FILE, 'r') as settings_file:
            settings = json.load(settings_file)["PhotoReceiver"]
            self._source = settings["photo_source"]

            if self._source == "local_dir":
                pass
            elif self._source == 'camera':
                pass

            else:
                raise RuntimeError(f'Unknown photo source {self._source}\n')

    def get_photo(self) -> str:
        """
        Получение пути к фотографии из очереди
        """
        return self._photo_queue.get()

    def _load_photo(self):
        """
        Загрузка фотографии в очередь из настроенного источника
        """
        if self._source == "camera":
            self._load_photo_from_camera()
        elif self._source == 'local_dir':
            self._load_photo_from_dataset()

    def _load_photo_from_dataset(self):
        """
        Загрузка фотографии в очередь из датасета
        """
        pass

    def _load_photo_from_camera(self):
        """
        Загрузка фотографии в очередь из подключённой камеры
        """