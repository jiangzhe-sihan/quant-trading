# NAME=保险轮动策略
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('open')
    self.set_price_sell('close')
    if not self.market.tell:
        return
    stock_list = list(self.market.tell.items())
    stock_list.sort(key=lambda x: x[1].increase)
    k = stock_list[0][0]
    if not self.warehouse:
        self.li_buy.add(k)
        return
    self.clear()
