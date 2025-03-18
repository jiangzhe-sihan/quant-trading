# NAME=强弩之末
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('跌停开', lambda x: x.open == x.dt_price(x.ref(1, 'close'), .1))
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            c = v.get_series('close')
            h = v.get_series('high')
            zt = c >= v.zt_price(v.ref(1, c), .1)
            dt = c <= v.dt_price(v.ref(1, c), .1)
            cci = v.get_series('cci')
            self.static[v.code] = v.ref(1, zt) & dt & (v.ref(1, cci) > 100) & (v.ref(1, v.hhv(5, h)) == v.ref(1, h))
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
