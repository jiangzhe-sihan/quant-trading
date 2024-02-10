# NAME=test
# DESCRIPTION=


prop = [
    ('振幅', lambda x: x.increase_day),
    ('量比', lambda x: x.lb),
    ('市值', lambda x: x.market_value),
    ('换手', lambda x: x.hs),
    ('index', lambda x: 10000 * x.lb * x.low / x.market_value)
]


def func(self):
    self.set_price_buy('open')
    self.set_price_sell('high')
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
            idx = 10000 * v.lb * v.low / v.market_value
            if (
                5.77 > idx > 5.45 or 4.44 > idx > 4.41 or 4.36 > idx > 4.31 or
                2.96 > idx > 2.93 or 2.9 > idx > 2.85 or 2.44 > idx > 2.42 or
                .65 > idx > .642 or .639 > idx > .636 or .635 > idx > .62 or 
                .591 > idx > .585 or .584 > idx > .58 or .552 > idx > .55 or 
                .533 > idx > .526 or .454 > idx > .451 or .415 > idx > .412 or 
                .361 > idx > .358 or .343 > idx > .336 or .324 > idx > .319 or 
                .251 > idx > .248 or .234 > idx > .233 or .17 > idx > .167 or 
                .124 > idx > .119 or .048 > idx > .046
                ):
                self.li_buy.add(k)
