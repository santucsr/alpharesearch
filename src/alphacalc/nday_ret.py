# Alpha01: n day return.
# we define the n day return for t0 to be return from t-(n+1) to t-1

# 
from datetime import datetime
from functools import partial
import logging
from multiprocessing import Pool
import warnings
warnings.filterwarnings('ignore')

#
import numpy as np
import pandas as pd

# Local Library imports
from utils.calendar import CALENDAR
from pathmgmt import pathmgmt as myPath
from loader import dataloader

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


def compute(start, end, window, universe, refresh=False):
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
    
    # function to compute return
    def compute_return(x):
        return np.log(x.shift(1)) - np.log(x.shift(1 + window))
    stocks['ret'] = stocks.groupby('code').adj_close.apply(compute_return)
    
    tableName = f"NdayReturn-{window}days-{universe}"
    (myPath.ALPHA_DIR/tableName).mkdir(parents=True, exist_ok=True)
    
    logger.debug(f"Start writing to files for alpha {tableName}...")
    
    dates = [d.strftime("%Y%m%d") for d in stocks.index.unique()]
    # ERROR: daemonic processes are not allowed to have children
    # with Pool() as pool:
    #     pool.map(partial(writeToFile, stocks, tableName, refresh),
    #              dates)
    for date in dates:
        writeToFile(stocks, tableName, refresh, date)
    logger.debug("Writing to files...Done!")
    # tips for nested functions and lambda expressions: https://gist.github.com/EdwinChan/3c13d3a746bb3ec5082f
    # https://stackoverflow.com/questions/20776189/concurrent-futures-vs-multiprocessing-in-python-3
    
    
def writeToFile(df, tab, refresh, date):
    outputfile = myPath.ALPHA_DIR/tab/(date+'.csv')
    if outputfile.exists() and not refresh:
        return
    try:
        df = df.loc[df.index==date].reset_index()
        df.time = df.time.dt.strftime("%Y%m%d")
        df = df[['time', 'code', 'name', 'ret']]
        df.to_csv(outputfile, index=False)
        logger.info(f"Writing to file on date {date} for alpha {tab}...Done!")
    except:
        logger.error(f"Exeption when Writing to file on date {date} for alpha {tab}")
        # error_list.append(name)
