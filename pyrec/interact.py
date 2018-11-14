import os
import sys
import logging
logger = logging.getLogger(__name__)
from .fileio import OpenFile
root_path = os.path.dirname(__file__)
commands = {}
logger = logging.getLogger(__name__)


class State(object):
    def __init__(self):
        self.dir_list = []


def command_handler(matchstr):
    def wrapper(func):
        commands[matchstr] = func
        logger.info('registered {} to {}'.format(func.__name__, matchstr))
        return func
    return wrapper


def function_connect(state, query):
    query_list = query.split(' ')

    try:
        state = commands[query_list[0]](state, query_list)
        return state
    except KeyError:
        print("can\'t understand query")
        return state
