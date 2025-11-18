# NAME=旱地拔葱
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('open')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        n = 20
        if v.code not in self.static:
            c = v.get_series('close')
            o = v.get_series('open')
            h = v.get_series('high')
            l = v.get_series('low')
            ma5 = v.ma(5, c)
            ma10 = v.ma(10, c)
            ma20 = v.ma(20, c)
            buy1 = v.between(ma5, o, c) & v.between(ma10, o, c) & v.between(ma20, o, c)
            buy2 = (ma5 > ma10) & (c > o) & (c / v.ref(1, c) < 1.04)
            buy3 = (ma5 > v.ref(1, ma5)) & (ma10 > v.ref(1, ma10)) & (ma20 > v.ref(1, ma20))
            cond1 = buy1 & buy2 & buy3
            vol = v.get_series('volume')
            inc = v.IF(c > o, h / l, l / h)
            _cond1 = inc > v.ref(1, inc)
            _cond2 = vol > v.ref(1, vol)
            up = v.count(_cond1 & _cond2, n) / v.count(_cond1, n)
            down = v.count(~(_cond1 | _cond2), n) / v.count(~_cond1, n)
            power = up + down
            pwm1 = v.ema(3, power)
            pwm2 = v.ema(14, power)
            cond2 = v.between(v.max(pwm1, pwm2), 1, 1.4)
            inc_p = c / v.ref(1, c) - 1
            a = v.ref(1, inc_p) + inc_p
            b = v.ref(1, a) + a
            lc = v.ref(1, b) + b
            d = v.std(3, lc)
            e = v.ema(60, d)
            cond3 = d > e
            self.static[v.code] = (
                cond1 & cond2 & cond3,
                c < ma5
            )
        if self.static[v.code][0][v.date]:
            self.li_buy.add(k)
            continue
        if self.static[v.code][1][v.date] and k in self.warehouse:
            self.li_sell.add(k)
