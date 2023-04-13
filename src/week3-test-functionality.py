from alphacalc import alpha_calc
from alpha_perfmc import perfmc

import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    # plots and daily pnl results will be saved in the plot folder    
    cfg_list = [('YaoMoM001', {'start_date': '20180101',
                           'end_date': '20201231',
                           'window': 5,
                           'universe': 'zz1000',
                           'refresh': True}),
                ('YaoMoM001', {'start_date': '20180101',
                          'end_date': '20201231',
                          'window': 5,
                          'universe': 'zz500',
                          'refresh': True}), 
                ('YaoMoM001', {'start_date': '20180101',
                          'end_date': '20201231',
                          'window': 5,
                          'universe': 'zz800',
                          'refresh': True}), 
                ('YaoMoM001', {'start_date': '20180101',
                            'end_date': '20201231',
                            'window': 5,
                            'universe': 'hs300',
                            'refresh': True}),]
    alpha_calc.calc(cfg_list)
    
    args_dict_list = [
        {
            'table_name': 'alpha.YaoMoM001-5days-zz1000',
            'start_date': '20180101',
            'end_date': '20201231',
            'transform': 'Rank',
            'neutralize': 'Industry'
        },        
        {
            'table_name': 'alpha.YaoMoM001-5days-zz800',
            'start_date': '20180101',
            'end_date': '20201231',
            'transform': 'Rank',
            'neutralize': 'Industry'
        },
        {
            'table_name': 'alpha.YaoMoM001-5days-zz500',
            'start_date': '20180101',
            'end_date': '20201231',
            'transform': 'Rank',
            'neutralize': 'Industry'
        },        
        {
            'table_name': 'alpha.YaoMoM001-5days-hs300',
            'start_date': '20180101',
            'end_date': '20201231',
            'transform': 'Rank',
            'neutralize': 'Industry'
        }
    ]
    perfmc.calc(args_dict_list)