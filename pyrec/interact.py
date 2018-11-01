import os
import sys
import logging
logger = logging.getLogger(__name__)
from .state import root_path, commands, command_handler
from .fileio import OpenFile


@command_handler('new_file')
def new_file(state, query_list):
    if(len(query_list) <= 1):
        logger.info('Input error; no file name;')
        return state
    log_path = os.path.join(os.path.dirname(root_path), 'log')
    for di in state.dir_list:
        log_path = os.path.join(log_path, di)
    log_path = os.path.join(log_path, query_list[1])
    with OpenFile() as f:
        f.open(log_path, 'r')  # r로 열어야 같은 이름 file 덮어쓰기 안함
        state.file_type = f.open_type
    return state


@command_handler('now_dir')
def now_dir(state, query_list):
    prstr = ''
    for i in range(0, len(state.dir_list)):
        prstr = pr_str + state.dir_list[i] + os.sep
    logger.info('location : log' + os.sep + prstr)
    prstr = os.listdir(os.path.join(os.path.dirname(root_path), 'log', prstr))
    logger.info(prstr)
    return state


@command_handler('quit')
def quit(state, query_list):
    logger.info('System quit')
    sys.exit()
    return 'ERROR?'


def function_connect(state, query):
    query_list = query.split(' ')

    try:
        state = commands[query_list[0]](state, query_list)
        return state
    except KeyError:
        print("can\'t understand query")
        return state
