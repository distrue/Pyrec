import os
import logging
from pyrec.interact import command_handler, root_path
from pyrec.fileio import OpenFile
from pyrec.signals import QueryError
from pyrec.manager import script_path
from .base import dir_check
from .parse import file_parse, load_script
logger = logging.getLogger(__name__)


@command_handler('find_script')
def find_script(state, query_list):
    if(len(query_list) <= 1):
        raise QueryError("find_script", "missing operator : name")
        # TODO : seperate write operation
    log_path = os.path.join(script_path, 'log')
    while(True):
        ans_list = []
        for ni in state.dir_list:
            dir_path = os.path.join(log_path, ni, 'script')
            for fi in os.listdir(dir_path):
                if(query_list[1] in fi):
                    ans_list.append([ni + ' / \'' + fi + '\'', os.path.join(dir_path, fi)])
        logger.info("choose operation : (0 : exit) (1 : read) (2: write) (3: delete)")
        x = input()
        try:
            x = int(x)
        except:
            logger.error("input must be integer type")
            continue
        if(x == 0):
            break
        elif(x == 1):
            while(True):
                logger.info("[script_show]0 : stop script_show")
                cou = 1
                for ni in ans_list:
                    logger.info('[script_show]' + str(cou) + ' : ' + ni[0])
                    cou += 1
                logger.info('[script_show] which script want to see?(in number)')
                x = input()
                try:
                    x = int(x)
                except:
                    logger.error("input must be integer type")
                    continue
                if(x == 0):
                    break
                elif(x >= cou):
                    logger.info("out of range")
                else:
                    with OpenFile() as f:
                        f.open(ans_list[x-1][1], 'r')
                        dump = f.read('text/plain')
                        logger.info('data\n' + dump)
        elif(x == 2):
            while(True):
                logger.info("choose dir to write, \q to quit")
                state = dir_check(state, ['show_dirs',])
                x = input()
                if('\q' in x):
                    break
                if(x not in state.dir_list):
                    logger.info("directory doesn\'t exist")
                    continue
                logger.info("open pyrec file : on run.py folder\npress any key to write file")
                new_path = os.path.join(script_path, 'new.pyrec')
                with OpenFile() as f:
                    f = open(new_path, 'w')
                y = input()
                dump = file_parse(new_path, [], 'pyrec')
                write_path = os.path.join(script_path, 'log', x, 'script')
                load_script(write_path, dump)
                os.remove(new_path)
                break
        elif(x == 3):
            while(True):
                logger.info("[script_show]0 : stop script_show")
                cou = 1
                for ni in ans_list:
                    logger.info('[script_show]' + str(cou) + ' : ' + ni[0])
                    cou += 1
                logger.info('[script_show] which script want to delete?(in number)')
                x = input()
                try:
                    x = int(x)
                except:
                    logger.error("input must be integer type")
                    continue
                if(x == 0):
                    break
                elif(x >= cou):
                    logger.info("out of range")
                else:
                    os.remove(ans_list[x-1][1])
                    logger.info('file deleted : ' + ans_list[x-1][1])
                    break
    return state
