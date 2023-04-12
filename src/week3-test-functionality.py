from alphacalc import alpha_calc
from alpha_perfmc import perfmc

if __name__ == "__main__":
    # cfg = [('NdayReturn', {'start': '20180101',
    #                       'end': '20201231',
    #                       'window': 30,
    #                       'universe': 'hs300',
    #                       'refresh': True}),
    #        ('NdayReturn', {'start': '20180101',
    #                       'end': '20201231',
    #                       'window': 60,
    #                       'universe': 'hs300',
    #                       'refresh': True}),
    #        ('NdayReturn', {'start': '20180101',
    #                       'end': '20201231',
    #                       'window': 90,
    #                       'universe': 'hs300',
    #                       'refresh': True}),
    #        ('NdayReturn', {'start': '20180101',
    #                        'end': '20201231',
    #                        'window': 30,
    #                        'universe': 'zz500',
    #                        'refresh': True}), 
    #        ('NdayReturn', {'start': '20180101',
    #                        'end': '20201231',
    #                        'window': 30,
    #                        'universe': 'zz800',
    #                        'refresh': True}),
    #        ('NdayReturn', {'start': '20180101',
    #                        'end': '20201231',
    #                        'window': 30,
    #                        'universe': 'zz1000',
    #                        'refresh': True}),]
    # # compute alphas
    # alpha_calc.calc(cfg)
    
    # # compute perfomance metrics for the computed alphas    
    # cfg_list = [#'alpha.NdayReturn-10days-hs300-20180101-20201231-10',
    #             'alpha.NdayReturn-30days-hs300-20180101-20201231-30',
    #             'alpha.NdayReturn-60days-hs300-20180101-20201231-30',
    #             'alpha.NdayReturn-90days-hs300-20180101-20201231-30',
    #             'alpha.NdayReturn-30days-zz500-20180101-20201231-30',
    #             'alpha.NdayReturn-30days-zz800-20180101-20201231-30',
    #             'alpha.NdayReturn-30days-zz1000-20180101-20201231-30']
    # pnl_calculator.calc(cfg_list)
    
    # # plots will be saved in the plot folder
    
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
                          'refresh': True}), ]
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
        }
    ]
    
    perfmc.calc(args_dict_list)