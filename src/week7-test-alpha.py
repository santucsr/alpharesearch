from alphacalc import alpha_calc
from alpha_perfmc import perfmc

import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    # plots and daily pnl results will be saved in the plot folder
    cfg_list = []
    for delay in [3, 5, 10, 20, 60]:
    # for delay in [20]:
        cfg_list.append(('YaoTec010', {'start_date': '20180101',
                                        'end_date': '20201231',
                                        'window': delay,
                                        'universe': 'zz9999',
                                        'refresh': True}))

    # alpha_calc.calc(cfg_list)

    args_dict_list = []
    # for delay in [3, 5, 10, 20, 60]:
    for delay in [20]:
        # for holdings in [1, 3, 5, 10, 20, 60]:
        for holdings in [1]:
            args_dict_list.append({
                'table_name': f'alpha.YaoTec009-{delay}days-zz9999',
                # 'table_name': f'alpha.YaoReV014-{delay}days-zz9999',
                'start_date': '20180101',
                'end_date': '20201231',
                'transform': 'None',
                'neutralize': 'None',
                'holding': holdings
            })
    perfmc.calc(args_dict_list)
#
