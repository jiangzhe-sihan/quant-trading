# NAME=ETF信号弹
# DESCRIPTION=提示各种etf的操作机会


prop = [
    ('close', lambda x: x.close),
    ('increase', lambda x: x.increase),
    ('increase_day', lambda x: x.increase_day),
    ('increase_width', lambda x: x.close / x.low - 1),
    ('ma5', lambda x: x.ma(5, 'close')),
    ('ma10', lambda x: x.ma(10, 'close')),
    ('ma5>ma10?', lambda x: x.ma(5, 'close') > x.ma(10, 'close')),
    ('bia5', lambda x: (x.close - x.ma(5, 'close')) / x.ma(5, 'close')),
    ('bia10', lambda x: (x.close - x.ma(10, 'close')) / x.ma(10, 'close')),
    ('bia_min_5', lambda x: (x.close - x.interval_min(5, 'close')) / x.interval_min(5, 'close')),
    ('bia_min_10', lambda x: (x.close - x.interval_min(10, 'close')) / x.interval_min(10, 'close')),
    ('bia_max_5', lambda x: (x.close - x.interval_max(5, 'close')) / x.interval_max(5, 'close')),
    ('bia_max_10', lambda x: (x.close - x.interval_max(10, 'close')) / x.interval_max(10, 'close')),
    ('bia_mid_10', lambda x: abs(x.close / x.interval_max(10, 'close') + x.close / x.interval_min(10, 'close') - 2)),
    ('tpp', lambda x: 2.5 * sum(x.atr()) + x.low)
]


def func(self):
    from configure import StrategyLoader
    sl = StrategyLoader('../strategies/ETFStrategyGroup/')
    self.static['ref'] = self.static.get('ref', {
        '501300': lambda: sl.get_strategy('dollar_bond_signal'),
        '512200': lambda: sl.get_strategy('fangdichan_signal'),
        '159752': lambda: sl.get_strategy('xinnengyuan_signal'),
        '512480': lambda: sl.get_strategy('bandaoti_signal'),
        '160723': lambda: sl.get_strategy('oil_signal'),
        '513100': lambda: sl.get_strategy('nasdaq_signal'),
        '510510': lambda: sl.get_strategy('zz500_signal'),
        '002837': lambda: sl.get_strategy('nvk')
    })
    for k, v in self.market.tell.items():
        name = k.split(']')[0].split('.')[1]
        # 测试
        # if name != '002837':
        #     continue
        # 调用
        f = self.static['ref'].get(name)
        if f is None:
            continue
        f().func(self, k, v)
