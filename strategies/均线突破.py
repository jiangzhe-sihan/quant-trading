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
    for k, v in self.market.tell.items():
        if v.code not in self.static:
            c = v.get_series('close')
            ma20 = v.ma(20, c)
            ma60 = v.ma(60, c)
            self.static[v.code] = v.cross(c, ma20) & (ma20 > ma60)
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
