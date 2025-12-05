# NAME=暴力洗盘
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
            vol = v.get_series('volume')
            fl = vol > v.ref(1, vol)
            o = v.get_series('open')
            l = v.get_series('low')
            cond = (c == o) & (l != c) & zt & fl
            self.static[v.code] = cond & ~v.ref(1, cond) & ~v.every(zt, 6)
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
