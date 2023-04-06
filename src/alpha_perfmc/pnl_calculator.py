
from datetime import datetime
import logging
from multiprocessing import Pool

import numpy as np
import pandas as pd

from loader import dataloader
from pathmgmt import pathmgmt as myPath
from . import metrics
from . import zscore


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


def compute_future_return(start, end, universe, holding_period):
    '''N day future return: return from t0 to t+N
    This is similar to the compute function in nday_ret'''
    logger.debug("Loading Cumulative Adjust Factor...")
    cum_adjf = dataloader.loading(
        'Cum Adj Factor', start, end=end, fields=['code', 'cum_adjf'])
    logger.debug("Loading Cumulative Adjust Factor...Done!")

    logger.debug("Loading Universe...")
    population = dataloader.loading(
        "Universe", start, end=end, fields=universe)
    logger.debug("Loading Universe...Done!")

    # TODO: loading from a rolling window
    logger.debug("Loading Stock PV...")
    # currently we are using close price to compute return
    # TODO: using different point in time to compute return
    stocks = dataloader.loading(
        tab_name="PV Basics", start=start, end=end, fields=['code', 'close'])
    logger.debug("Loading Stock PV...Done!")

    # merge PV data with adj factor
    stocks = stocks.reset_index().merge(cum_adjf.reset_index(),
                                        on=['time', 'code'], how='left').set_index('time')

    # select stocks in the universe
    stocks = stocks.reset_index().merge(population.reset_index(),
                                        on=['time', 'code'], how='inner').set_index('time')
    # adj close
    stocks['adj_close'] = stocks['close'] * stocks['cum_adjf']

    # compute future return
    stocks['fut_ret_1d'] = stocks.groupby('code').adj_close.transform(
        lambda x: np.log(x.shift(-1)) - np.log(x))
    stocks[f'fut_ret_{holding_period}d'] = stocks.groupby('code').adj_close.transform(
        lambda x: np.log(x.shift(-holding_period)) - np.log(x))
    
    return stocks


def compute_pnl(tab_name, start, end, universe, holding_period):
    '''As the first cut, we make the following assumption:
    if the holding period is N > 1, we still assume daily rebalance,
    but in each day, we only invest 1/N of the today capital
    we also assume we have already transformed zscores into weights/positions'''

    positions = zscore.alpha_to_zscore(tab_name, start, end)
    returns = compute_future_return(start, end, universe, holding_period)

    positions = positions.reset_index().merge(returns.reset_index(),
                                        on=['time', 'code'], how='left').set_index('time')
    
    # rolling rum of the zscores
    rolling = positions.groupby('code').zscores.rolling(
        holding_period, min_periods=1).sum().reset_index()
    rolling['zscores'] = rolling['zscores'] / holding_period
    rolling.rename(columns={'zscores': 'rolling_zscores'}, inplace=True)
    positions = positions.reset_index().merge(rolling.reset_index(),
                               on=['time', 'code'], how='left').set_index('time')
    
    # compute pnl
    positions['pnl'] = positions['rolling_zscores'] * positions['fut_ret_1d']
    
    # compute performance metrics
    # here we assume benchmark is the universe
    metrics.compute_matrics(
        positions, tab_name, start, end, universe, holding_period)
    # daily_pnl, statistics = metrics.compute_matrics(
    #     positions, tab_name, start, end, universe, holding_period)

    # return positions, daily_pnl,  statistics

def doCompute(cfg):
    args = cfg.split('-')
    tab_name = "-".join([args[0], args[1], args[2]])
    universe = args[2]
    start = args[3]
    end = args[4]
    holding_period = int(args[5])
    logger.debug(f"computing pnl for {tab_name} from {start} to {end} with a holding period of {holding_period} days...")
    # pnl = compute_pnl(tab_name, start, end, universe, holding_period)
    compute_pnl(tab_name, start, end, universe, holding_period)
    logger.debug("compute pnl...Done!")
    # return pnl
    
def calc(cfg_list):
    '''cfg_list = ['alphaname-(args)-universe-start-end-holding', ...]
    '''
    # multiprocessing
    with Pool() as pool:
        pool.map(doCompute, cfg_list)
        
    # return pnl
