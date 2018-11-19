import signal
import logging
import sys
logger = logging.getLogger(__name__)  # __name__ 통한 호출>


def sigint_handler(signum, frame):
    logger.info('SIGINT inputed(ctrl+c)')
    sys.exit()


class QueryError(Exception):
    def __init__(self):
        logger.error('query syntax error')
        # logging.error('ss') 와의 차이점?


signal.signal(signal.SIGINT, sigint_handler)  # sigint_handler
# TODO : windows sigint?
