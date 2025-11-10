# System imports
import sys
import signal

# External imports

# User imports
from consts import signals
from factories import ResourcesStorage
from utils import MessagesToMain, AppLogger
from messages_to_main_checker import MessagesToMainChecker


##########################################################


def enf_of_program(signum, frame):
    resource_storage = ResourcesStorage()
    app_logger = AppLogger()

    app_logger.info(f'Signal {signals[signum]} has been received')
    resource_storage.cleanup_all()

    app_logger.info(f'ResourcesStorage:\n'
                    f'{resource_storage}')

    sys.exit(0)
