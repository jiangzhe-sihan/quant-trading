# NAME=原地飞升
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('close', lambda x: x.close)
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
            o = v.get_series('open')
            inc = c / v.ref(1, c) - 1
            cond = v.between(v.count(inc, 5), .1, .15) & (c > o)
            self.static[v.code] = cond & ~v.ref(1, cond)
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
