import os
import pyrec
import logging
import sys
import signal
logger = logging.getLogger(__name__)  # __name__ 통한 호출>


if __name__ == '__main__' :
    kw = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.INFO,
        'stream': sys.stdout,
    }
    logging.basicConfig(**kw)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
    logger.info('Pyrec V0.1')
    state = pyrec.state.State()
    while(True):
        print('$ ', end = '')
        try:
            in_str = input()
            state = pyrec.interact.function_connect(state, in_str)
        except EOFError:
            break

"""
    with pyrec.fileio.OpenFile() as f:
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(file_path, data, 'd.json')
        f.open(file_path, 'r')
"""
