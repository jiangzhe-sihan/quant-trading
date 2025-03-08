# NAME=rsi超卖
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('市值', lambda x: x.market_value)
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        df = (v.ref(10, 'close') - v.close) / v.ref(10, 'close') > .25
        xy = (min(v.open, v.close) - v.low) / (v.high - v.low) > .7 if v.high - v.low else False
        xg = df and xy and v.rsi(6) < 20
        if xg:
            self.li_buy.add(k)
