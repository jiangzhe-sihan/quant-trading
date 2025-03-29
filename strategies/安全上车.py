# NAME=安全上车
# DESCRIPTION=


prop = [
    ('倍量', lambda x: x.volume / x.ref(1, 'volume')),
    ('市值', lambda x: x.market_value),
    ('lwr', lambda x: x.lwr())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    itv = 60
    m1 = 12
    m2 = 144
    m3 = 169
    m4 = 576
    m5 = 676
    for k, v in self.market.tell.items():
        if not v.market_value > 40000000000:
            continue
        if v.increase > 0 and v.ref(1, 'volume') and v.volume / v.ref(1, 'volume') > 1.52 and v.hhv(15, 'high') != v.high:
            up = v.count(lambda x: x.increase_day > 0, itv)
            up_ex = v.count(lambda x: x.increase_day > 0 and x.volume > x.ref(1, 'volume'), itv)
            down = v.count(lambda x: x.increase_day < 0, itv)
            down_ex = v.count(lambda x: x.increase_day < 0 and x.volume < x.ref(1, 'volume'), itv)
            c1, c2 = up / up_ex if up_ex else 0, down / down_ex if down_ex else 0
            if c1 > .8 and c2 > .8 and c1 + c2 > 1.8:
                em1 = v.ema(m1, 'close')
                em2 = v.ema(m2, 'close')
                em3 = v.ema(m3, 'close')
                em4 = v.ema(m4, 'close')
                em5 = v.ema(m5, 'close')
                sdv = (em2 + em3) / 2
                qsv = (em4 + em5) / 2
                ref_qsv = (v.ref(1, 'ema', m4, 'close') + v.ref(1, 'ema', m5, 'close')) / 2
                if v.close > sdv and em1 > sdv and qsv > ref_qsv:
                    self.li_buy.add(k)
