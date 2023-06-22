from alphacalc import alpha_calc
from alpha_perfmc import perfmc

import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    args_dict_list = []
    for holdings in [1, 3, 5, 10, 20, 60]:
        args_dict_list.append({
            'table_name': f'alpha.combined-lvl2-equalweight-zz9999',
            'start_date': '20180101',
            'end_date': '20201231',
            'transform': 'None',
            'neutralize': 'Industry',
            'holding': holdings
        })
        args_dict_list.append({
            'table_name': f'alpha.combined-lvl2-irweight-zz9999',
            'start_date': '20180101',
            'end_date': '20201231',
            'transform': 'None',
            'neutralize': 'Industry',
            'holding': holdings
        })
    perfmc.calc(args_dict_list)