# NAME=ex-boll
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('pwm1', lambda x: x.ema(3, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20))[x.date]),
    ('pwm2', lambda x: x.ema(14, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20))[x.date]),
    ('vrsi', lambda x: 100 * x.ema(10, x.sma(10, 1, x.max(x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20) - x.ref(1, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20)), 0)) / x.sma(10, 1, abs(x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20) - x.ref(1, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20)))))[x.date])
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    nb = 20
    m = 2
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            c = v.get_series('close')
            mid = v.ema(nb, c)
            lower = mid - m * v.std(nb, c)
            upper = mid + m * v.std(nb, c)
            l = v.get_series('low')
            h = v.get_series('high')
            self.static[v.code] = v.cross(l, lower)
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
