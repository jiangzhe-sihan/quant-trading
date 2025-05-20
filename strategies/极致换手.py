# NAME=极致换手
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('close', lambda x: x.close),
    ('pwm1', lambda x: x.ema(3, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20))[x.date]),
    ('pwm2', lambda x: x.ema(14, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20))[x.date]),
    ('vrsi', lambda x: 100 * x.ema(10, x.sma(10, 1, x.max(x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20) - x.ref(1, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20)), 0)) / x.sma(10, 1, abs(x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20) - x.ref(1, x.count((x.get_series('close') / x.ref(1, x.get_series('close')) > 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) > 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) > 1, 20) + x.count((x.get_series('close') / x.ref(1, x.get_series('close')) <= 1) & (x.get_series('volume') / x.ref(1, x.get_series('volume')) < 1), 20) / x.count(x.get_series('close') / x.ref(1, x.get_series('close')) <= 1, 20)))))[x.date])
]


def func(self):
    self.set_price_buy('open')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if 60 > v.hs > 40 and v.close < v.open and v.cci() < 150 and v.count(lambda x: True, 60) == 60:
            self.li_buy.add(k)
    self.clear()
