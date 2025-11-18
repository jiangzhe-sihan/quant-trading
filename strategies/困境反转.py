# NAME=困境反转
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('open')
    self.set_price_sell('high')
    n = 20
    span = 14
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            c = v.get_series('close')
            # o = v.get_series('open')
            vol = v.get_series('volume')
            inc = c / v.ref(1, c)
            vinc = vol / v.ref(1, vol)
            up = v.count((inc > 1) & (vinc > 1), n) / v.count(inc > 1, n)
            down = v.count((inc <= 1) & (vinc < 1), n) / v.count(inc <= 1, n)
            power = up + down
            pwm1 = v.ema(3, power)
            pwm2 = v.ema(14, power)
            buy1 = v.every(v.max(pwm1, pwm2) < .9, span)
            inc_p = inc - 1
            a = v.ref(1, inc_p) + inc_p
            b = v.ref(1, a) + a
            lc = v.ref(1, b) + b
            d = v.std(3, lc)
            e = v.ema(60, d)
            buy2 = v.count(d > e, span) / span > .5
            self.static[v.code] = buy1 & buy2
        if self.static[v.code][v.date] and v.amount > 50000000:
            self.li_buy.add(k)
