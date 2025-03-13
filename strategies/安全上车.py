# NAME=安全上车
# DESCRIPTION=


prop = [
    ('倍量', lambda x: x.volume / x.ref(1, 'volume')),
    ('市值', lambda x: x.market_value),
    ('lwr', lambda x: x.lwr())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    itv = 60
    for k, v in self.market.tell.items():
        if v.increase > 0 and v.ref(1, 'volume') and v.volume / v.ref(1, 'volume') > 1.52 and v.hhv(15, 'high') != v.high and v.close > v.ma(5, 'high'):
            up = v.count(lambda x: x.increase_day > 0, itv)
            up_ex = v.count(lambda x: x.increase_day > 0 and x.volume > x.ref(1, 'volume'), itv)
            down = v.count(lambda x: x.increase_day < 0, itv)
            down_ex = v.count(lambda x: x.increase_day < 0 and x.volume < x.ref(1, 'volume'), itv)
            c1, c2 = up / up_ex if up_ex else 0, down / down_ex if down_ex else 0
            if c1 > .8 and c2 > .8 and c1 + c2 > 1.8:
                self.li_buy.add(k)
