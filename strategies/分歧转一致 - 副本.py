# NAME=分歧转一致
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
        if v.code not in self.static:
            c = v.get_series('close')
            zt = c >= v.zt_price(v.ref(1, c), .1)
            db = v.ref(1, zt) & ~zt
            vol = v.get_series('volume')
            fl = vol > v.ref(1, vol)
            self.static[v.code] = v.ref(1, db & fl) & zt & ~fl
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
