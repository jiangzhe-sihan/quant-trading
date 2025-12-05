# NAME=小群战法
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
            vol = v.get_series('volume')
            _3b = v.every(zt, 3)
            cond = _3b & ~v.ref(1, _3b) & (vol > 2 * v.ma(20, vol)) & (c < 10)
            self.static[v.code] = cond
        if self.static[v.code][v.date]:
            self.li_buy.add(k)
