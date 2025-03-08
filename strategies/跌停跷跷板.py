# NAME=跌停跷跷板
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        if f'dt_{v.code}' not in self.static:
            dt = v.get_series('close') <= v.dt_price(v.ref(1, v.get_series('close')), .1)
            self.static[f'dt_{v.code}'] = dt
        dt = self.static[f'dt_{v.code}']
        if v.ref(1, dt)[v.date] and v.volume / v.ref(1, 'volume') > 10:
            self.li_buy.add(k)
