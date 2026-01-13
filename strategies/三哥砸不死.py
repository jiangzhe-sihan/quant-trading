# NAME=三哥砸不死
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('open')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        # Write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        # Use series datas like this:
        # ```
        # if v.code not in self.static:
        #     c = v.get_series('close')
        #     cond = v.cross(c, v.ma(5, c))
        #     self.static[v.code] = cond
        # if self.static[v.code][v.date]:
        #     self.li_buy.add(k)
        # ```
        if v.code not in self.static:
            c = v.get_series('close')
            zt = c >= v.zt_price(v.ref(1, c), .1)
            sb = v.every(zt, 2)
            l = v.get_series('low')
            cond = v.ref(1, sb & ~v.ref(1, sb)) & (l / v.ref(1, c) - 1 < -.08)
            self.static[v.code] = cond
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
