# NAME=对齐颗粒度
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    n = 20
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
            buy2 = v.cross(pwm1, pwm2) | v.cross(pwm2, pwm1)
            buy_all = (buy1 & buy2) | (buy1 & v.ref(1, buy2)) | (buy2 & v.ref(1, buy1))
            hc = v.between(inc, .94, .98)
            zt = c >= v.zt_price(v.ref(1, c), .06)
            cci = v.get_series('cci')
            self.static[v.code] = buy_all & (v.count(buy2, n) / n < .2) & (v.ref(0, v.exist(zt, 3))) & (v.ref(1, v.exist(hc, 5))) & (cci > v.ref(1, cci))
        if self.static[v.code][v.date] and v.amount > 50000000:
            self.li_buy.add(k)
