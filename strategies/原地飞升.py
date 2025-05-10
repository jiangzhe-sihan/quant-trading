# NAME=原地飞升
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('open')
    self.set_price_sell('high')
    n = 20
    nr = 10
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
            stick = (c / o - 1) / (inc - 1)
            self.static[v.code] = (v.max(pwm1, pwm2) > 1.1) & (vrsi > 46) & (inc - 1 > .5) & (c > 1) & (stick > .5)
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
