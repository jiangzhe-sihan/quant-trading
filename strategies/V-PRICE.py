# NAME=V-PRICE
# DESCRIPTION=成交量加权平均价波段策略


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            amo = v.get_series('amount')
            vol = v.get_series('volume')
            x = 100 if v.code[0] == 's' else 1
            v_price = amo / vol / x
            close = v.get_series('close')
            self.static[v.code] = (
                v.cross(close, v_price),
                v.cross(v_price, close)
            )
        if self.static[v.code][0][v.date]:
            self.li_buy.add(k)
            continue
        if self.static[v.code][1][v.date]:
            self.li_sell.add(k)
