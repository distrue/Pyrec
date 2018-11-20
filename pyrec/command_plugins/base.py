import os
import logging
import sys
from pyrec.interact import command_handler, root_path
from pyrec.fileio import OpenFile
from .load import package_script_load
logger = logging.getLogger(__name__)
from .parse import lookup_dir
from pyrec.signals import QueryError


@command_handler('pwd')
def pwd(state, query_list):
    now_path = os.path.dirname(os.path.dirname(__file__))
    logger.info(now_path)
    return state


@command_handler('open_dir')
def open_dir(state, query_list):
    with OpenFile() as f:
        if(query_list <= 1):
            QueryError('open_dir', 'missing argument : file_path')
        if(os.path.exists(query_list[1])):
            if(len(query_list) <= 2):
                dir_name = 'new'
                cou = 1
                now_path = os.path.dirname(os.path.dirname(__file__))
                log_path = os.path.join(now_path, 'log')
                while(os.path.exists(os.path.join(log_path, dir_name + str(cou)))):
                    cou += 1
                query_list.append(dir_name + str(cou))
            pyrec_data = os.path.join(query_list[1], '.pyrec')
            if(not os.path.exists(pyrec_data)):
                os.makedirs(pyrec_data)
            refresh(state, query_list)
            logger.info('new dir created : ' + file_name)
        else :
            QueryError('open_dir', "file does not exists in : " + query_list[1] + '\nwe need an abspath')
        return state
    # .pyrec 로드
    # file load 하는 state에 pyrec의 원본 폴더 위치 저장


"""
[구현 함수]
- script 내의 하이퍼링크 기능 구현
# 먼저 봐야 하는 script 설정해주기
- html, md 형태로 변환해주는 script 제작
- data 를 압축할 수 있는 방안 마련, data 삭제 방안
-> remote 가 아닌 local log 중 특정 상태일 떄만
- Script 검색
- 1) name 검색
- 2) keyword 검색
- 지정된 script 출력 -> 이전 명령어가 script 검색인 경우 cli에서 다른 형태로 질의하게 지정
/// file 위치로 이동해서 #s_script 부터 #e_script 까지 보여준다.
- 키워드 검색 시 자동완성 기능 (키워드 묶음을 유기적으로 구성하기 위해 필요)
"""
# TODO : log의 분리 : 사용자가 접근할 수 있는 local folder 필요


@command_handler('refresh')
def refresh(state, query_list):
    if(query_list <= 1):
        QueryError('refresh', 'missing argument : file_path')
    elif(query_list <= 2):
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
    # for file_walker in os.walk(query_list[1]):
    #    print(file_walker)
        # os.walk 실행 시 (위치, [folders], [files]) 의 형태로 전순회 된다.
    with OpenFile() as f:
        now_path = os.path.dirname(os.path.dirname(__file__))
        log_path = os.path.join(now_path, 'log', query_list[2], 'script_tree.json')
        f.open(log_path, 'w')
        dump = lookup_dir(query_list[1], ignore_syntax)
        f.write(dump, 'application/json')
        # (나중에는 git 처럼 diff check 방식으로)


@command_handler('quit')
def quit(state, query_list):
    logger.info('System quit')
    sys.exit()
    return 'Quit ERROR occured'
