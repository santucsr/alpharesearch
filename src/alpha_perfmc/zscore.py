
from datetime import datetime
import logging

import numpy as np
import pandas as pd

from loader import dataloader
from pathmgmt import pathmgmt as myPath


logFormatter = logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

LogPath = myPath.makeLogPath(datetime.now(), __name__)

fileHandler = logging.FileHandler(LogPath)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.setLevel(logging.DEBUG)

# we can implement different methods to translate alphas into weights
def alpha_to_zscore(tab_name, start, end):
    logger.debug(f"Loading alphas for {tab_name} from {start} to {end}...")
    alphas = dataloader.loading(
        tab_name, start=start, end=end, fields=['code', 'name', 'ret'])
    logger.debug(f"Loading alphas for {tab_name} from {start} to {end}...Done!")
    # TODO: other methods to compute zscore
    logger.debug(f"Compute zscores...")
    zscores = rank(alphas)
    logger.debug(f"Compute zscores...Done!")
    
    return zscores

# one implementation using rank
def rank(alphas):
    alphas['ranks'] = alphas.groupby('time').ret.transform(
        lambda x: x.sort_values(ascending=True).rank(ascending=True, method="max"))
    alphas['ranks'] = alphas.groupby(
        'time').ranks.transform(lambda x: x - x.mean())
    alphas['zscores'] = alphas.groupby(
        'time').ranks.transform(lambda x: x / x.abs().sum())
    return alphas
