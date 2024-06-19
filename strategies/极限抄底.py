# NAME=极限抄底
# DESCRIPTION=


prop = [
    ('qta', lambda v: v.increasement(v.interval_max(3, 'open'), v.close)),
    ('lwr', lambda x: x.lwr())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        lwr1, lwr2 = v.lwr()
        inc = v.increase
        qta = v.increasement(v.interval_max(3, 'open'), v.close)
        jxcd = (v.interval_min(3, 'increase') == inc and lwr1 > lwr2 and qta < -.039 and 
                (lwr1 - lwr2) * (lwr1 + lwr2) > 350 and v.interval_max(3, 'high') != v.high and 
                v.close > 18)
        if jxcd and 'ST' not in k:
            self.li_buy.add(k)
