# NAME=均线突破（不吃香菜）
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    n = 20
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            c = v.get_series('close')
            ma20 = v.ema(20, c)
            ma60 = v.ema(60, c)
            dif = ma20 - ma60
            vol = v.get_series('volume')
            inc = c - v.ref(1, c)
            up = v.count((inc > 0) & (vol > v.ref(1, vol)), n) / v.count(inc > 0, n)
            down = v.count((inc <= 0) & (vol < v.ref(1, vol)), n) / v.count(inc <= 0, n)
            power = up + down
            self.static[v.code] = (ma20 > ma60) & v.cross(c, ma20) & (dif > v.ref(1, dif)) & (power > 1.2) & (v.min(up, down) > .6)
        if self.static[v.code][v.date] and (v.market_value > 40000000000 or v.close > 20):
            self.li_buy.add(k)
