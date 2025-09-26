import multiprocessing as mp
from multiprocessing import Queue, Process
import time
from typing import Any, Callable, Optional, Dict
from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    COMMAND = "command"
    RESULT = "result"
    LOG = "log"


@dataclass
class Message:
    type: MessageType
    payload: Any = None
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class AsyncMethodExecutor:
    """
    Универсальный исполнитель методов в отдельном процессе
    с поддержкой callback'ов для событий
    """

    def __init__(self, target_object: Any, method_name: str):
        self.target_object = target_object
        self.method_name = method_name
        self.method = getattr(target_object, method_name)

        self.process: Optional[Process] = None
        self.command_queue = Queue()
        self.result_queue = Queue()

        self.callbacks = {
            'on_start': None,
            'on_result': None,
            'on_error': None,
            'on_finish': None
        }

    def set_callback(self, event: str, callback: Callable):
        """Установка callback'а для события"""
        if event in self.callbacks:
            self.callbacks[event] = callback

    def _run_method(self, *args, **kwargs):
        """Внутренний метод, запускаемый в процессе"""
        # Callback запуска
        if self.callbacks['on_start']:
            self.result_queue.put(Message(MessageType.LOG, "Метод запущен"))

        try:
            # Выполняем целевой метод
            result = self.method(*args, **kwargs)

            # Отправляем результат
            self.result_queue.put(Message(MessageType.RESULT, result))

            # Callback успешного завершения
            if self.callbacks['on_finish']:
                self.result_queue.put(Message(MessageType.LOG, "Метод завершен успешно"))

        except Exception as e:
            # Callback ошибки
            error_msg = f"Ошибка в методе {self.method_name}: {str(e)}"
            self.result_queue.put(Message(MessageType.ERROR, error_msg))

    def start(self, *args, **kwargs) -> bool:
        """Запуск метода в отдельном процессе"""
        if self.process and self.process.is_alive():
            return False

        self.process = Process(
            target=self._run_method,
            args=args,
            kwargs=kwargs,
            daemon=True
        )
        self.process.start()
        return True

    def stop(self) -> bool:
        """Остановка процесса"""
        if not self.process or not self.process.is_alive():
            return False

        self.process.terminate()
        self.process.join(timeout=5)
        return True

    def get_results(self) -> list[Message]:
        """Получение всех результатов"""
        results = []
        while not self.result_queue.empty():
            try:
                message = self.result_queue.get_nowait()
                results.append(message)

                # Вызываем соответствующие callback'и
                if message.type == MessageType.RESULT and self.callbacks['on_result']:
                    self.callbacks['on_result'](message.payload)
                elif message.type == MessageType.ERROR and self.callbacks['on_error']:
                    self.callbacks['on_error'](message.payload)

            except:
                break
        return results

    def is_running(self) -> bool:
        return self.process and self.process.is_alive()


# Пример использования с callback'ами
class DataAnalyzer:
    def __init__(self, name: str):
        self.name = name

    def analyze(self, data: list) -> Dict[str, Any]:
        """Пример аналитического метода"""
        time.sleep(1)  # Имитация долгой работы

        return {
            'analyzer': self.name,
            'data_length': len(data),
            'sum': sum(data) if all(isinstance(x, (int, float)) for x in data) else None,
            'average': sum(data) / len(data) if data else 0
        }


def on_result(result):
    print(f"📊 Получен результат анализа: {result}")


def on_error(error):
    print(f"❌ Ошибка: {error}")


def on_start():
    print("🚀 Запуск анализа...")


def example_usage():
    # Создаем объект для анализа
    analyzer = DataAnalyzer("StatisticalAnalyzer")

    # Создаем исполнитель
    executor = AsyncMethodExecutor(analyzer, "analyze")

    # Настраиваем callback'и
    executor.set_callback('on_result', on_result)
    executor.set_callback('on_error', on_error)

    # Запускаем анализ
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    executor.start(test_data)

    # Мониторим результаты
    while executor.is_running():
        executor.get_results()  # Вызовет callback'и автоматически
        time.sleep(0.1)

    # Получаем финальные результаты
    final_results = executor.get_results()
    for msg in final_results:
        print(f"Финальное сообщение: {msg}")


if __name__ == "__main__":
    example_usage()