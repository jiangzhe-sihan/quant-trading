# NAME=止盈止损
# DESCRIPTION=模拟条件单


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    for k, v in self.warehouse.items():
        if v.income_pct > .02 or v.income_pct < -.02:
            self.li_sell.add(k)
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        pass
