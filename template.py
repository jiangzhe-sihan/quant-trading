import datetime

from framework import KLine


def get_strategy_template(name: str, desc: str):
    res = f"""# NAME={name}
# DESCRIPTION={desc}


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        pass
"""
    return res


def get_kline_test_example():
    it = [
        (datetime.datetime(2015, 1, 1), {'open': 1, 'high': 2, 'low': 0, 'close': 1, 'volume': 100}),
        (datetime.datetime(2015, 1, 2), {'open': 1, 'high': 2, 'low': 0, 'close': 1, 'volume': 100}),
        (datetime.datetime(2015, 1, 3), {'open': 1, 'high': 2, 'low': 0, 'close': 1, 'volume': 100}),
        (datetime.datetime(2015, 1, 4), {'open': 1, 'high': 2, 'low': 0, 'close': 1, 'volume': 100}),
        (datetime.datetime(2015, 1, 5), {'open': 1, 'high': 2, 'low': 0, 'close': 1, 'volume': 100}),
    ]
    res = None
    for i in it:
        k = KLine(*i)
        if res is None:
            res = k
            continue
        res.insert(k)
    return res


def get_strategy_path():
    return '../strategies/'


def get_logging_path():
    return 'log.txt'


class CommonPool:
    refer = {
        '** 沪深主板 **': 'fs=m:0+t:6+f:!2,m:1+t:2+f:!2',
        '** 创业板 **': 'fs=m:0+t:80+f:!2',
        '** 科创板 **': 'fs=m:1+t:23+f:!2',
        '** 美  股 **': 'fs=m:105+t:1,m:105+t:3,m:106+t:1,m:106+t:3,m:107+t:1,m:107+t:3',
        '** 港  股 **': 'fs=m:116+t:3',
        '** 复杂杠杆 **': 'fs=m:105+t:5,m:106+t:5,m:107+t:5',
    }
