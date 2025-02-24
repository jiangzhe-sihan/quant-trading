# NAME=macd_index
# DESCRIPTION=


prop = [
    ('macd', lambda x: x.macd())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        macd = v.macd()[2]
        ref_macd = v.ref(1, 'macd')[2]
        if macd > 0 and ref_macd < 0:
            self.li_buy.add(k)
        elif macd < 0 and ref_macd > 0:
            self.li_sell.add(k)
