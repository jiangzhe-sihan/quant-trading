# NAME=极致换手
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
        if 60 > v.hs > 40 and v.close < v.open and v.cci() < 150 and v.count(lambda x: True, 60) == 60:
            self.li_buy.add(k)
    self.clear()
