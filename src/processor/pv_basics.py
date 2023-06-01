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

def processConsistentVolume(data):
    '''Function to generate the consistent volume feature'''
    a = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    columns = ['code'] + [f'consistent_volume_{i}' for i in a]
    consistent_volumes = []
    for i in a:
        consistent_volumes.append((data.volume * ((data.open - data.close).abs()
                                                < (data.high - data.low).abs() * i) * (data.time <= 1457)).sum())
    return [data.iloc[0].code] + consistent_volumes, columns

def processConsistentBuySell(data):
    '''Function to generate the consistent volume feature'''
    a = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    columns = ['code'] + [f'consistent_buy_{i}' for i in a] + [f'consistent_sell_{i}' for i in a]
    consistent_volumes = []
    for i in a:
        consistent_volumes.append((data.volume * ((data.open - data.close).abs()
                                                  < (data.high - data.low).abs() * i) * (data.time <= 1457) * (data.close > data.open)).sum())
    for i in a:
        consistent_volumes.append((data.volume * ((data.open - data.close).abs()
                                                  < (data.high - data.low).abs() * i) * (data.time <= 1457) * (data.close < data.open)).sum())
    return [data.iloc[0].code] + consistent_volumes, columns

def processBuySellVolume(data):
    pass

def processBuySellTurnover(data):
    columns = ['code'] + ['buy_turnover'] + ['sell_turnover']
    turnovers = []
    turnovers.append((data.turover * (data.time <= 1457) * (data.close > data.open)).sum())
    turnovers.append((data.turover * (data.time <= 1457) * (data.close < data.open)).sum())
    return [data.iloc[0].code] + turnovers, columns

def processConsistentBuySellTurnover(data):
    '''Function to generate the consistent turnover feature'''
    a = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    columns = ['code'] + [f'consistent_buy_trv_{i}' for i in a] + [f'consistent_sell_trv_{i}' for i in a]
    consistent_turnover = []
    for i in a:
        consistent_turnover.append((data.turover * ((data.open - data.close).abs()
                                                  < (data.high - data.low).abs() * i) * (data.time <= 1457) * (data.close > data.open)).sum())
    for i in a:
        consistent_turnover.append((data.turover * ((data.open - data.close).abs()
                                                  < (data.high - data.low).abs() * i) * (data.time <= 1457) * (data.close < data.open)).sum())
    return [data.iloc[0].code] + consistent_turnover, columns

def processConsistentTurnover(data):
    '''Function to generate the consistent volume feature'''
    a = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    columns = ['code'] + [f'consistent_turnover_{i}' for i in a]
    consistent_turnover = []
    for i in a:
        consistent_turnover.append((data.turover * ((data.open - data.close).abs()
                                                  < (data.high - data.low).abs() * i) * (data.time <= 1457)).sum())
    return [data.iloc[0].code] + consistent_turnover, columns
