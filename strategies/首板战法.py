# NAME=对齐颗粒度
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('cci', lambda x: x.cci()),
    ('bl', lambda x: x.volume / x.ref(1, 'volume')),
    ('lb', lambda x: x.lb)
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
            vol = v.get_series('volume')
            inc = c / v.ref(1, c)
            vinc = vol / v.ref(1, vol)
            up = v.count((inc > 1) & (vinc > 1), n) / v.count(inc > 1, n)
            down = v.count((inc <= 1) & (vinc < 1), n) / v.count(inc <= 1, n)
            power = up + down
            pwm1 = v.ema(3, power)
            pwm2 = v.ema(14, power)
            buy2 = v.between(v.max(pwm1, pwm2), 1, 1.4)
            inc_p = inc - 1
            a = v.ref(1, inc_p) + inc_p
            b = v.ref(1, a) + a
            lc = v.ref(1, b) + b
            d = v.std(3, lc)
            e = v.ema(60, d)
            zt = c >= v.zt_price(v.ref(1, c), .1)
            h = v.get_series('high')
            czt = h >= v.zt_price(v.ref(1, c), .1)
            mvol = v.ma(5, vol)
            lb = vol / v.ref(1, mvol)
            self.static[v.code] = (
                zt & ~v.ref(1, czt) & (v.exist(buy2, 3) | (pwm1 > v.ref(1, pwm1))) & v.exist(v.cross(d, e), 4) & v.between(lb, 1.1, 1.5)
            )
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
