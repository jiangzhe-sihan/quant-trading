# NAME=test
# DESCRIPTION=


prop = [
    ('振幅', lambda x: x.increase_day),
    ('量比', lambda x: x.lb),
    ('市值', lambda x: x.market_value),
    ('换手', lambda x: x.hs)
]


def func(self):
    self.set_price_buy('open')
    self.set_price_sell('open')
    s = 20
    m = 40
    n = 60
    self.clear()
    for k, v in self.market.tell.items():
        if v.close > v.open and (
            v.close > v.ma(s, 'close') and v.close > v.ma(m, 'close') and v.close > v.ma(n, 'close')
        ) and (
            v.open < v.ma(m, 'close') and v.open < v.ma(n, 'close')
        ) and v.close - v.open > .0618 * v.close:
            self.li_buy.add(k)
