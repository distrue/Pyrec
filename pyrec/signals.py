import signal
import logging
import sys
import traceback
logger = logging.getLogger(__name__)  # __name__ 통한 호출>


def getTracebackStr():
	lines = traceback.format_exc().strip().split('\n')
	rl = [lines[-1]]
	lines = lines[1:-1]
	lines.reverse()
	for i in range(0,len(lines),2):
		rl.append('^\t%s at %s' % (lines[i].strip(),lines[i+1].strip()))
	return '\n'.join(rl)


def sigint_handler(signum, frame):
    logger.info('SIGINT inputed(ctrl+c)')
    sys.exit()


class QueryError(Exception):
    def __init__(self, query='unknown', reason='unknown'):
        logger.error('{}query syntax error; '.format(query) + reason)
        # logging.error('ss') 와의 차이점?


signal.signal(signal.SIGINT, sigint_handler)  # sigint_handler
# TODO : windows sigint?
