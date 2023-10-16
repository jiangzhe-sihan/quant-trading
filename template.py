import datetime

from framework import KLine


def get_strategy_template(name: str, desc: str):
    res = f"""# NAME={name}
# DESCRIPTION={desc}


prop = []


def func(self):
    for k, v in self.market.tell.items():
        # write your strategy here
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
