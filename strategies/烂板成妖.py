# NAME=烂板成妖
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
    ('cci', lambda x: x.cci())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if 60 > v.hs > 40 and v.close >= v.zt_price(v.ref(1, 'close'), .1) and v.count(lambda x: True) > 60:
            self.li_buy.add(k)
    self.clear()
