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
    pyrec.manager.run(os.path.abspath(__file__))
