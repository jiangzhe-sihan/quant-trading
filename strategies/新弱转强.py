# NAME=新弱转强
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('cci', lambda x: x.cci())
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
            vol = v.get_series('volume')
            inc = c - v.ref(1, c)
            up = v.count((inc > 0) & (vol > v.ref(1, vol)), n) / v.count(inc > 0, n)
            down = v.count((inc <= 0) & (vol < v.ref(1, vol)), n) / v.count(inc <= 0, n)
            power = up + down
            pwm1 = v.ema(3, power)
            pwm2 = v.ema(14, power)
            h = v.get_series('high')
            zt = c >= v.zt_price(v.ref(1, c), .1)
            cci = v.get_series('cci')
            self.static[v.code] = (v.cross(pwm1, pwm2) | v.cross(pwm2, pwm1)) & (h != v.hhv(7, h)) & (v.count(zt, 7) > 0) & (cci > v.ref(1, cci))
        if self.static[v.code][v.date] and v.amount > 50000000:
            self.li_buy.add(k)
