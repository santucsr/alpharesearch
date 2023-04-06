# 
from datetime import datetime
import logging
from multiprocessing import Pool
from . import nday_ret

# Local 
from pathmgmt import pathmgmt as myPath

logFormatter = logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

LogPath = myPath.makeLogPath(datetime.now(), __name__)

fileHandler = logging.FileHandler(LogPath)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
logger.setLevel(logging.DEBUG)

FUNCTIONS = {'NdayReturn': nday_ret.compute}

def compute_single_alpha(cfg):
    algo, kwargs = cfg
    FUNCTIONS[algo](**kwargs)

def calc(cfg_dict):
    '''cfg_dict is a lisg: [(alpha_name, **kwargs), ...]'''
    # multiprocess here
    with Pool() as pool:
        pool.map(compute_single_alpha, cfg_dict)
