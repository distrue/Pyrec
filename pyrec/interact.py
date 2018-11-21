import os
import sys
import logging
logger = logging.getLogger(__name__)
from .fileio import OpenFile
from .signals import QueryError, getTracebackStr
root_path = os.path.dirname(__file__)
commands = {}
logger = logging.getLogger(__name__)
from pyrec.manager import script_path


class State(object):
    def __init__(self):
        self.dir_list = []  # 현재 open 되어 있는 dir들

    def load(self):
        log_path = os.path.join(script_path, 'log')
        for ni in os.listdir(log_path):
            self.dir_list.append(ni)


def command_handler(matchstr):
    def wrapper(func):
        commands[matchstr] = func
        logger.info('registered {} to {}'.format(func.__name__, matchstr))
        return func
    return wrapper


def function_connect(state, query):
    _query_list = query.split(' ')
    query_list = []
    try:
        for _query in _query_list:
            if(_query):
                query_list.append(_query)
    except QueryError:
        return state
    try:
        if(query_list[0] not in commands):
            logger.info('uncensored query ' + query_list[0])
            return state
        state = commands[query_list[0]](state, query_list)
        return state
    except QueryError:
        return state
    except SystemExit:
        logger.info('System Exit')
        raise SystemExit
    except:
        logger.error(getTracebackStr())
        return state
        # state 가 변하지 않았다고 가정한다.
