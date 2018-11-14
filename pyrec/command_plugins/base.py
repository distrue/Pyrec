import os
import logging
from pyrec.interact import command_handler, root_path
from pyrec.fileio import OpenFile
logger = logging.getLogger(__name__)

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
        prstr = prstr + state.dir_list[i] + os.sep
    logger.info('location : log' + os.sep + prstr)
    prstr = os.listdir(os.path.join(os.path.dirname(root_path), 'log', prstr))
    logger.info(prstr)
    return state


@command_handler('quit')
def quit(state, query_list):
    logger.info('System quit')
    sys.exit()
    return 'ERROR?'
