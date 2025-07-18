# NAME=一倍大的夹头
# DESCRIPTION=bushi（


prop = [
    # ('index_name', lambda x: x.func())
    ('bl', lambda x: x.volume / x.ref(1, 'volume'))
]


def func(self):
    self.set_price_buy('open')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        n = 20
        nr = 12
        if v.code not in self.static:
            c = v.get_series('close')
            vol = v.get_series('volume')
            inc = c / v.ref(1, c)
            vinc = vol / v.ref(1, vol)
            up = v.count((inc > 1) & (vinc > 1), n) / v.count(inc > 1, n)
            down = v.count((inc <= 1) & (vinc < 1), n) / v.count(inc <= 1, n)
            power = up + down
            pwm1 = v.ema(3, power)
            pwm2 = v.ema(14, power)
            cond1 = v.between(v.max(pwm1, pwm2), 1, 1.4)
            mid = v.ema(n, c)
            upper = mid + 2 * v.std(n, c)
            lower = mid - 2 * v.std(n, c)
            width = upper - lower
            cond2 = v.every(width < v.ref(1, width), nr)
            mvol = v.ma(n, vol)
            cond3 = v.every(mvol > v.ref(1, mvol), nr)
            self.static[v.code] = cond1 & cond2 & cond3 & v.between(c, upper, lower)
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
