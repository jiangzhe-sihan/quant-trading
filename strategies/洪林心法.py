# NAME=洪林心法
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('open')
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
            tb = v.every(zt, 2)
            cond = tb & ~v.ref(1, tb)
            vol = v.get_series('volume')
            self.static[v.code] = v.ref(1, cond) & (vol > v.ref(1, vol))
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
        if k in self.warehouse and v.increase < 0:
            self.li_sell.add(k)
