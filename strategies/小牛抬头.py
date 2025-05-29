# NAME=小牛抬头
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('code', lambda x: x.code),
    ('name', lambda x: x.name),
    ('bl', lambda x: x.volume / x.ref(1, 'volume')),
    ('bool-up', lambda x: x.close / (x.ma(20, 'close') + 2 * x.std(20, 'close')) - 1)
]


def func(self):
    self.set_price_buy('low')
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
            sync = inc / vinc
            masy = v.ema(n, v.ema(n, sync))
            difsy = 10 * (masy - v.ref(1, masy))
            chg = difsy * v.ref(1, difsy) < 0
            dif = c - o
            buy1 = (chg & (difsy * dif < 0))
            up = v.count((inc > 1) & (vinc > 1), n) / v.count(inc > 1, n)
            down = v.count((inc <= 1) & (vinc < 1), n) / v.count(inc <= 1, n)
            power = up + down
            pwm1 = v.ema(3, power)
            pwm2 = v.ema(14, power)
            difp = power - v.ref(1, power)
            vrsi = 100 * v.ema(nr, v.sma(nr, 1, v.max(difp, 0)) / v.sma(nr, 1, abs(difp)))
            code = v.code.split('.')[1]
            ztr = .2 if code.startswith('30') or code.startswith('68') else .05 if 'ST' in v.name else .1
            zt = c >= v.zt_price(v.ref(1, c), ztr)
            bl = vol / v.ref(1, vol)
            self.static[v.code] = ((v.max(pwm1, pwm2) > 1.1) | (vrsi > 46)) & zt & ~v.ref(1, v.exist(zt, 10)) & v.exist(buy1, 2) & ~v.between(bl, 2.5, 4)
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
