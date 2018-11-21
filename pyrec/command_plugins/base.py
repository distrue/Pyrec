import os
import logging
import sys
from pyrec.interact import command_handler, root_path
from pyrec.fileio import OpenFile
logger = logging.getLogger(__name__)
from .parse import lookup_dir
from pyrec.signals import QueryError
from pyrec.manager import script_path


@command_handler('pwd')
def pwd(state, query_list):
    # __name__ : 절대 경로를 포함한 python package 실행, package 밖에서 실행되면 __main__ 또는 주소
    # __file__ : 현재 file의 절대 경로
    # __package__ : package 내에 있을 떄의 경로
    logger.info(script_path)
    return state


@command_handler('open_dir')
def open_dir(state, query_list):
    if(len(query_list) <= 1):
        QueryError('open_dir', 'missing argument : file_path')
    if(os.path.exists(query_list[1])):
        if(len(query_list) <= 2):
            dir_name = 'new'
            cou = 1
            now_path = script_path
            log_path = os.path.join(now_path, 'log')
            while(os.path.exists(os.path.join(log_path, dir_name + str(cou)))):
                cou += 1
            query_list.append(dir_name + str(cou))
        pyrec_data = os.path.join(query_list[1], '.pyrec')
        if(not os.path.exists(pyrec_data)):
            os.makedirs(pyrec_data)
        refresh(state, query_list)
        logger.info('new dir created : ' + query_list[2])
    else :
        QueryError('open_dir', "file does not exists in : " + query_list[1] + '\nwe need an abspath')
    state.load()
    return state
    # .pyrec 로드
    # file load 하는 state에 pyrec의 원본 폴더 위치 저장


"""
[구현 함수]
- script 내의 하이퍼링크 기능 구현 -> 위상 정렬 구현
- html, md 형태로 변환해주는 script 제작
- Script 검색
1) name 검색
2) keyword 검색
- 키워드 검색 시 자동완성 기능 (키워드 묶음을 유기적으로 구성하기 위해 필요)
"""


@command_handler('refresh')
def refresh(state, query_list):
    if(len(query_list) <= 1):
        QueryError('refresh', 'missing argument : file_path')
    elif(len(query_list) <= 2):
        QueryError('refresh', 'missing argument : file_name')
    if(not os.path.exists(query_list[1])):
        logger.error("file does not exists in : " + query_list[1])
        return state
    ignore_path = os.path.join(query_list[1], '.pyrec', '.ignore')
    ignore_syntax = []
    if(os.path.exists(ignore_path)):
        with OpenFile() as f:
            f.open(ignore_path, 'r')
            dump = f.read()
            ignore_syntax.extend(dump.split('\n'))
    # s_script os.walk
    # for file_walker in os.walk(query_list[1]):
    #    print(file_walker)
        # os.walk 실행 시 (위치, [folders], [files]) 의 형태로 전순회 된다.
    # e_script
    now_path = script_path
    log_path = os.path.join(now_path, 'log', query_list[2], 'script')
    lookup_dir(log_path, query_list[1], ignore_syntax)
    state.load()
    return state
    # (나중에는 git 처럼 diff check 방식으로)


@command_handler('show_dirs')
def dir_check(state, query_list):
    prstr = '<<dir lists>>\n'
    cou = 0
    for ni in state.dir_list:
        prstr += ni + ' '
        if(cou >= 5):
            cou -= 5
            prstr += '\n'
        cou += 1
    logger.info(prstr)
    return state


@command_handler('find_script')
def find_script(state, query_list):
    if(len(query_list) <= 1):
        raise QueryError("find_script", "missing operator : name")
    log_path = os.path.join(script_path, 'log')
    ans_list = []
    for ni in state.dir_list:
        dir_path = os.path.join(log_path, ni, 'script')
        for fi in os.listdir(dir_path):
            if(query_list[1] in fi):
                ans_list.append([ni + ' / \'' + fi + '\'', os.path.join(dir_path, fi)])
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
        else:
            with OpenFile() as f:
                f.open(ans_list[x-1][1], 'r')
                dump = f.read('text/plain')
                logger.info('data\n' + dump)
    return state


@command_handler('rm_dir')
def rm_dir(state, query_list):
    if(len(query_list) <= 1):
        raise QueryError('rm_dir', 'missing argument; dir_name')
    log_path = os.path.join(script_path, 'log', query_list[1])
    if(not os.path.exists(log_path)):
        logger.info('directory does not exists')
        return state
    import shutil
    shutil.rmtree(log_path)
    logger.info('directory [' + query_list[1] + '] deleted')
    state.load()
    return state


@command_handler('quit')
def quit(state, query_list):
    sys.exit()
    return 'Quit ERROR occured'
