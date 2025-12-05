# NAME=步步高升
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('open')
    self.set_price_sell('high')
    n = 20
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            c = v.get_series('close')
            ma5 = v.ma(5, c)
            incp = c / v.ref(1, c) - 1
            a = v.ref(1, incp) + incp
            b = v.ref(1, a) + a
            lc = v.ref(1, b) + b
            d = v.std(3, lc)
            e = v.sma(60, 1, d)
            o = v.get_series('open')
            h = v.get_series('high')
            l = v.get_series('low')
            vol = v.get_series('volume')
            inc = v.IF(c > o, h / l, l / h)
            cond1 = inc > v.ref(1, inc)
            cond2 = vol > v.ref(1, vol)
            up = v.count(cond1 & cond2, n) / v.count(cond1, n)
            down = v.count(~(cond1 | cond2), n) / v.count(~cond1, n)
            power = up + down
            pwm1 = v.ema(3, power)
            pwm2 = v.ema(14, power)
            inc1 = 10000 * v.IF(incp > 0, v.max(incp, h / l - 1), v.min(incp, l / h - 1))
            vinc = abs(inc1 / vol)
            pwm = v.ema(n, v.ema(n, vinc > v.ref(1, vinc)))
            cond = v.every(c > ma5, 4) & v.every(d < e, 10) & (v.min(pwm1, pwm2) > .8) & (v.max(pwm1, pwm2) < 1.3) & v.IF(incp > 0, pwm < .5, pwm > .5)
            self.static[v.code] = cond & ~v.ref(1, cond)
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
