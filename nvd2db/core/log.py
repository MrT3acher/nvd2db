import coloredlogs
import logging


from .config import LOG_PATH


def set_log_level(level, colored=True):
    format = '%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s'
    filehandler = logging.FileHandler(LOG_PATH, mode='a')
    formatter = coloredlogs.BasicFormatter(format)
    filehandler.setFormatter(formatter)
    logging.root.addHandler(filehandler)

    if colored:
        coloredlogs.install(level=level, fmt=format)
    else:
        logging.basicConfig(level=level)
