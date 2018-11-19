import os
import sys
import logging
logger = logging.getLogger(__name__)
from .fileio import OpenFile
from .signals import QueryError
root_path = os.path.dirname(__file__)
commands = {}
logger = logging.getLogger(__name__)


class State(object):
    def __init__(self):
        self.open_dir = []  # 현재 open 되어 있는 project들
        self.dir_path = {}  # open 되어 있는 project의 root directory, root directory 안에 .pyrec 폴더를 가짐.
        # TODO : local_data directory 생성
        # TODO : 현재 log 안에 있는 data load
        # 저장 위치 : 'local_data': os.path.join(os.path.dirname(__file__), 'log', 'local_data')
        # 저장 위치를 다음과 같이 분리 : log 안에 
        # - data : local_data와 실제로 옮겨온 project들
        # - pyrec_load : pyrec syntax를 기준으로 로드해온 key file


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
                raise QueryError()
                # query syntax error시 syntax error 발행
    except QueryError:
        return state
    try:
        state = commands[query_list[0]](state, query_list)
        return state
    except KeyError:
        print("unsensored query [" + query_list[0] + "]")
        return state
    except Exception as E:
        print("unexpected error")
        return state
        # state 가 변하지 않았다고 가정한다.
