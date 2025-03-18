# NAME=均线突破
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('hs', lambda x: x.hs),
    ('rsi6', lambda x: x.rsi(6)),
    ('cci', lambda x: x.cci())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    if 'obs' not in self.static:
        self.static['obs'] = set()
    obs = self.static['obs']
    n = 20
    for k, v in self.market.tell.items():
        if v.code not in self.static:
            c = v.get_series('close')
            l = v.get_series('low')
            o = v.get_series('open')
            vol = v.get_series('volume')
            ma20 = v.ma(20, c)
            ma60 = v.ma(60, c)
            up = v.count((c > v.ref(1, c)) & (vol > v.ref(1, vol)), n) / v.count(c > v.ref(1, c), n)
            down = v.count((c < v.ref(1, c)) & (vol < v.ref(1, vol)), n) / v.count(c < v.ref(1, c), n)
            self.static[v.code] = (
                v.cross(c, ma20) & (ma20 > ma60) & (up + down < 1.3), 
                v.between(ma20, l, v.min(c, o)) & (ma20 > ma60),
                v.cross(v.max(ma20, ma60), c)
            )
        if self.static[v.code][0][v.date] and v.amount > 50000000 and v.close > 20 and v.cci() < 90:
            obs.add(k)
            continue
        if k in obs and self.static[v.code][1][v.date]:
            self.li_buy.add(k)
            obs.remove(k) if k in obs else None
            continue
        if self.static[v.code][2][v.date]:
            self.li_sell.add(k)
            obs.remove(k) if k in obs else None
            continue
