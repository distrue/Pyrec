import os
import logging
root_path = os.path.dirname(__file__)
commands = {}
logger = logging.getLogger(__name__)


class State(object):
    def __init__(self):
        self.dir_list = []
        self.file_type = ''


def command_handler(matchstr):
    def wrapper(func):
        commands[matchstr] = func
        logger.info('registered {} to {}'.format(func.__name__, matchstr))
        return func
    return wrapper
