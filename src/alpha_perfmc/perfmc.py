
from multiprocessing import Pool

from alpha_perfmc import calculator

def doCompute(cfg):
    calcObj = calculator.PnLCalculator(cfg)
    calcObj.compute_pnl()

def calc(cfg_list):
    '''cfg_list = [args_dict, ...]
    '''
    # multiprocessing here
    with Pool() as pool:
        pool.map(doCompute, cfg_list)
