# NAME=三相之力
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('cci', lambda x: x.cci()),
    ('rsi', lambda x: x.rsi(6)),
    ('日内涨幅', lambda x: x.increase_day)
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
            sig = v.cross(pwm1, pwm2) | v.cross(pwm2, pwm1)
            # l = v.get_series('low')
            # bot = (v.llv(4, l) == l) | (v.llv(4, c) == c)
            buy2 = sig
            difp = power - v.ref(1, power)
            vrsi = 100 * v.ema(nr, v.sma(nr, 1, v.max(difp, 0) / v.sma(nr, 1, abs(difp))))
            buy3 = v.ref(1, vrsi < v.ref(1, vrsi)) & (vrsi > v.ref(1, vrsi))
            # filter = ((dif <= 0) | (inc < 1)) & (vol > v.ref(1, vol))
            # self.static[v.code] = ~filter & v.ref(2, v.exist(buy2, 2)) & buy1 & buy3
            filter = (v.get_series('cci') > 40) & (dif / o > .01) & (inc > 1.05)
            self.static[v.code] = filter & ((buy2 & buy1 & v.ref(1, buy3)) | (buy2 & buy3 & v.ref(1, buy1)))
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
