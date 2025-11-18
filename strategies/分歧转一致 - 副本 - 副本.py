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
            inc = c / v.ref(1, c) - 1
            zt = inc > 0
            db = v.ref(1, zt) & ~zt
            vol = v.get_series('volume')
            fl = vol > v.ref(1, vol)
            ma5 = v.ma(5, c)
            self.static[v.code] = db & fl & v.every(c > ma5, 2)
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
