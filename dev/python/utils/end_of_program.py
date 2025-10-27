# System imports
import sys
import signal

# External imports

# User imports
from consts import signals
from factories import ResourcesStorage
from utils import MessagesToMain
from messages_to_main_checker import MessagesToMainChecker


##########################################################


def enf_of_program(signum, frame):
    resource_storage = ResourcesStorage()

    print(f'Получен сигнал {signals[signum]}')
    resource_storage.cleanup_all()

    print(f'ResourcesStorage:\n'
          f'{resource_storage}')
    print(f'MessagesToMain().qsize(): {MessagesToMain().qsize()}')

    sys.exit(0)
