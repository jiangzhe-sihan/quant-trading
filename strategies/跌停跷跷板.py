# NAME=跌停跷跷板
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        if v.code not in self.static:
            c = v.get_series('close')
            dt = c <= v.dt_price(v.ref(1, c), .1)
            vol = v.get_series('volume')
            self.static[v.code] = v.ref(1, dt) & (vol / v.ref(1, vol) > 10)
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
