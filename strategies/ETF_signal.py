# NAME=ETF信号弹
# DESCRIPTION=提示各种etf的操作机会


prop = [
    ('open', lambda x: x.open),
    ('high', lambda x: x.high),
    ('low', lambda x: x.low),
    ('close', lambda x: x.close),
]


def func(self):
    from configure import StrategyLoader
    sl = StrategyLoader('../strategies/ETFStrategyGroup/')
    stg_dlb = sl.get_strategy('dollar_bond_signal')
    stg_fdc = sl.get_strategy('fangdichan_signal')
    stg_xny = sl.get_strategy('xinnengyuan_signal')
    stg_bdt = sl.get_strategy('bandaoti_signal')
    stg_oil = sl.get_strategy('oil_signal')
    stg_ndq = sl.get_strategy('nasdaq_signal')
    stg_zz500 = sl.get_strategy('zz500_signal')
    for k, v in self.market.tell.items():
        if '501300' in k:
            stg_dlb.func(self, k, v)
        elif '512200' in k:
            stg_fdc.func(self, k, v)
        elif '159752' in k:
            stg_xny.func(self, k, v)
        elif '512480' in k:
            stg_bdt.func(self, k, v)
        elif '160723' in k:
            stg_oil.func(self, k, v)
        elif '513100' in k:
            stg_ndq.func(self, k, v)
        elif '510510' in k:
            stg_zz500.func(self, k, v)
