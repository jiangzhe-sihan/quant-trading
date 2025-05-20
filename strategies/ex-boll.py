# NAME=ex-boll
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('pwm1', lambda x: x.ema(3, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20))[x.date]),
    ('pwm2', lambda x: x.ema(14, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20))[x.date]),
    ('vrsi', lambda x: 100 * x.ema(10, x.sma(10, 1, x.max(x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20) - x.ref(1, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20)), 0)) / x.sma(10, 1, abs(x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20) - x.ref(1, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20)))))[x.date])
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    nb = 20
    m = 2
    n = 20
    nr = 10
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            c = v.get_series('close')
            mid = v.ema(nb, c)
            # lower = mid - m * v.std(n, c)
            upper = mid + m * v.std(nb, c)
            # l = v.get_series('low')
            h = v.get_series('high')
            vol = v.get_series('volume')
            inc = c / v.ref(1, c)
            vinc = vol / v.ref(1, vol)
            up = v.count((inc > 1) & (vinc > 1), n) / v.count(inc > 1, n)
            down = v.count((inc <= 1) & (vinc < 1), n) / v.count(inc <= 1, n)
            power = up + down
            pwm1 = v.ema(3, power)
            pwm2 = v.ema(14, power)
            difp = power - v.ref(1, power)
            vrsi = 100 * v.ema(nr, v.sma(nr, 1, v.max(difp, 0)) / v.sma(nr, 1, abs(difp)))
            self.static[v.code] = v.cross(h, upper) & v.between(v.max(pwm1, pwm2), 1.1, 1.2) & (vrsi > 30)
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
