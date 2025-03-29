# NAME=对齐颗粒度
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('cci', lambda x: x.cci()),
    ('bl', lambda x: x.volume / x.ref(1, 'volume'))
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    n = 20
    # if 'li_buy' not in self.static:
    #     self.static['li_buy'] = set()
    # li_buy = self.static['li_buy']
    # if li_buy:
    #     self.li_buy.update(li_buy)
    #     li_buy.clear()
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            c = v.get_series('close')
            o = v.get_series('open')
            h = v.get_series('high')
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
            buy2 = v.cross(pwm1, pwm2) | v.cross(pwm2, pwm1)
            zt = c >= v.zt_price(v.ref(1, c), .1)
            self.static[v.code] = (
                buy1 & zt & (v.exist(buy2, 3) | (pwm1 > v.ref(1, pwm1))) & 
                v.ref(3, v.hhv(2, h) != h) & v.ref(6, ~v.exist(zt, 3)) & 
                (v.count(buy2, n) / n < .2) & (v.between(vinc, 1.22, 1.99) | (vinc > 3))
            )
        if self.static[v.code][v.date] and v.market_value > 3000000000 and v.count(lambda x: True) > 60 and v.hs < 13:
            self.li_buy.add(k)
