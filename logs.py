import logging.handlers
import sys

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler(sys.stdout)
f_handler = logging.FileHandler('file.log')
r_handler = logging.handlers.SysLogHandler(address=('10.0.32.65', 514))

c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.INFO)
r_handler.setLevel(logging.WARNING)

c_format = logging.Formatter('%(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
r_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
r_handler.setFormatter(f_format)

logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.addHandler(r_handler)

if __name__ == '__main__':
    logger.info('info')
    logger.debug('debug')
    logger.warning('warning')
    logger.error('error')
    logger.critical('crit')
