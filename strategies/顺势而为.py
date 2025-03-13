# NAME=顺势而为
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('up', lambda x: x.count(lambda v: v.close > v.ref(1, 'close') and v.volume > v.ref(1, 'volume'), 20) / x.count(lambda v: v.close > v.ref(1, 'close'), 20)),
    ('down', lambda x: x.count(lambda v: v.close <= v.ref(1, 'close') and v.volume < v.ref(1, 'volume'), 20) / x.count(lambda v: v.close <= v.ref(1, 'close'), 20))
]


def func(self):
    from numpy import nan
    self.set_price_buy('low')
    self.set_price_sell('high')
    n = 20
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            c = v.get_series('close')
            vol = v.get_series('volume')
            inc = c - v.ref(1, c)
            up = v.count((inc > 0) & (vol > v.ref(1, vol)), n) / v.count(inc > 0, n)
            down = v.count((inc <= 0) & (vol < v.ref(1, vol)), n) / v.count(inc <= 0, n)
            if len(up) != len(down):
                print(v.code)
            rsi6 = v.get_series('rsi', 6)
            ma20 = v.ma(20, c)
            ma60 = v.ma(60, c)
            self.static[v.code] = (up + down > 1) & (v.min(up, down) > .6) & (rsi6 < .2) & (ma20 > ma60)
        if self.static[v.code][v.date] and v.amount > 50000000 and v.close > 50:
            self.li_buy.add(k)
