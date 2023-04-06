# Standard
import numpy as np

def process1min(data):
    '''write a function to iterate all names in one date folder
    Main functionality to generate features
    '''
    column_names = ['code', 'open', 'close', 'pre_close',
                    'low', 'high', 'open_std',
                    'close_std', 'total_volume', 'total_turnover', 'volume_std', 'turnover_std']
    # TODO: sprecial handling for 0 value??
    open = data.iloc[0].open
    close = data.iloc[-1].close
    pre_close = data.iloc[0].pre_close
    low = data.low.min()
    high = data.high.max()
    # 1 min return volatility
    open_std = data.open.pct_change().replace(
        [np.inf, -np.inf], np.nan).dropna().std()
    close_std = data.close.pct_change().replace(
        [np.inf, -np.inf], np.nan).dropna().std()
    total_volume = data.iloc[-1].accvolume
    total_turnover = data.iloc[-1].accturover
    volume_std = data.volume.std()
    turnover_std = data.turover.std()  # typo here?
    return [data.iloc[0].code, open, close, pre_close, low, high, open_std, close_std, total_volume, total_turnover, volume_std, turnover_std], column_names
