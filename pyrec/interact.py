import os
import sys
import logging
logger = logging.getLogger(__name__)
from .fileio import OpenFile
from .signals import QueryError, getTracebackStr
root_path = os.path.dirname(__file__)
commands = {}
logger = logging.getLogger(__name__)
# s_script errorshoot_cycle import
# package import 내에서 cycle이 발생하는 경우가 있다. 이 경우는 error 발생, 이를 방지하기 위해서 각 file의 위상 설정이 필요하다.
# ex) from pyrec.manager import script_path -> 이미 manager에서 현재 file을 import하고 있기 때문에 import 하면 안된다.
# package 내의 package 에서 상위의 함수가 필요한 경우는 package 순회 중의 loop가 발생하지 않으므로 영향을 받지 않는다.
# 이 경우에 하위 package에서 import 한 값은 import 지점에서 값이 바뀌면 같이 값이 바뀐다.
# e_script


class State(object):
    def __init__(self, script_path):
        self.dir_list = []  # 현재 open 되어 있는 dir들
        self.script_path = script_path

    def load(self):
        self.dir_list = []
        log_path = os.path.join(self.script_path, 'log')
        if(os.path.exists(log_path)):
            for ni in os.listdir(log_path):
                if(ni not in self.dir_list):
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
