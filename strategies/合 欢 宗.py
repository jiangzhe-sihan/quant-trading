# NAME=合 欢 宗
# DESCRIPTION=指抱团（bushi


prop = [
    # ('index_name', lambda x: x.func())
    ('a', lambda x: x.count(lambda y: y.increase, 5)),
    ('b', lambda x: x.count(lambda y: y.increase_day, 5)),
    ('bl', lambda x: x.volume / x.ref(1, 'volume')),
    ('hs', lambda x: x.hs),
    ('zf', lambda x: x.close / x.llv(5, 'close') - 1),
    ('fl', lambda x: x.count(lambda x: x.volume, 4) / x.count(lambda x: x.volume, 14))
]


def func(self):
    self.set_price_buy('open')
    self.set_price_sell('high')
    n = 20
    nr = 10
    rg = 10
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            c = v.get_series('close')
            o = v.get_series('open')
            vol = v.get_series('volume')
            inc = c / v.ref(1, c)
            vinc = vol / v.ref(1, vol)
            up = v.count((inc > 1) & (vinc > 1), n) / v.count(inc > 1, n)
            down = v.count((inc <= 1) & (vinc < 1), n) / v.count(inc <= 1, n)
            power = up + down
            pwm1 = v.ema(3, power)
            pwm2 = v.ema(14, power)
            difp = power - v.ref(1, power)
            vrsi = 100 * v.ema(nr, v.sma(nr, 1, v.max(difp, 0) / v.sma(nr, 1, abs(difp))))
            a = v.count(c / o - 1, rg)
            b = v.count(inc - 1, rg)
            stick = abs(a / b)
            bl = vol / v.ref(1, vol)
            hs = v.get_series('hs')
            zt = c >= v.zt_price(v.ref(1, c), .1)
            zf = c / v.llv(5, c) - 1
            fl = v.count(vol, 4) / v.count(vol, 14)
            self.static[v.code] = ((v.max(pwm1, pwm2) > 1.1) | (vrsi > 36)) & (stick > .65) & (bl < 1.9) & (c >= o) & (inc > 1.03) & (~zt | (hs < 5.9)) & (zf > .15) & ~v.between(fl, .33, .55)
        if self.static[v.code][v.date] and v.hs > 5:
            self.li_buy.add(k)
