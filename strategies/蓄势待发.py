# NAME=蓄势待发
# DESCRIPTION=bushi（


prop = [
    # ('index_name', lambda x: x.func())
    ('code', lambda x: x.code),
    ('bl', lambda x: x.volume / x.ref(1, 'volume')),
    ('pwm1', lambda x: x.ema(3, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20))[x.date]),
    ('pwm2', lambda x: x.ema(14, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20))[x.date]),
    ('vrsi', lambda x: 100 * x.ema(10, x.sma(10, 1, x.max(x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20) - x.ref(1, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20)), 0)) / x.sma(10, 1, abs(x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20) - x.ref(1, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20)))))[x.date])
]


def func(self):
    self.set_price_buy('open')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        n = 20
        nr = 60
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
            tpw = v.max(pwm1, pwm2)
            mid = v.ma(n, c)
            upper = mid + 2 * v.std(n, c)
            buy = (v.count(tpw > v.ref(1, tpw), nr) / nr > .55) & (tpw < 1.4) & (pwm1 > pwm2) & (c < upper)
            self.static[v.code] = buy & ~v.ref(1, buy)
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
