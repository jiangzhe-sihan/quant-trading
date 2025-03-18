# NAME=弱转强
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('cci', lambda x: x.cci())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    n = 3
    m = 2
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            c = v.get_series('close')
            o = v.get_series('open')
            h = v.get_series('high')
            vol = v.get_series('volume')
            zt = c >= v.zt_price(v.ref(1, c), .1)
            rstj = (v.count(c < o, n) == n) | (v.count(c / v.ref(1, c) < .97, n) >= 2)
            jrgk = v.between(o / v.ref(1, c), 1.02, 1.05)
            fltp = (vol > v.ref(1, vol) * m) & (c > o * 1.03)
            fbyx = (c > v.ref(1, h)) & (v.ref(1, c) < v.ref(1, o)) & (c > o)
            self.static[v.code] = rstj & ((jrgk & fltp) | fbyx) & (v.count(zt, 7) > 0)
        if self.static[v.code][v.date] and v.cci() > 0:
            self.li_buy.add(k)
