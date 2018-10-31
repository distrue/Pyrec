import os
import sys
import logging
logger = logging.getLogger(__name__)


def new_file(state, query_list):
    if(len(query_list) <= 1) :
        logger.info('Input error; no file name;\n', end='')
        return state
    logger.info(os.path.dirname(__file__))
    logger.info('On development')
    return state


def now_dir(state, query_list):
    for i in range(0, state.dir_depth):
        logger.info(state.dir_list[i], end=os.sep)
    return state


def quit(state, query_list):
    logger.info('System quit')
    sys.exit()
    return 'ERROR?'


def function_connect(state, query):
    query_list = query.split(' ')
    query_call = {}
    query_call['new_file'] = new_file  # TODO : decorator로 전환
    query_call['now_dir'] = now_dir
    query_call['quit'] = quit

    try:
        state = query_call[query_list[0]](state, query_list)
        return state
    except KeyError:
        print("can\'t understand query")
        return state
