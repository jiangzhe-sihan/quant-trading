# NAME=Vegas隧道
# DESCRIPTION=


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    m1 = 12
    m2 = 144
    m3 = 169
    m4 = 576
    m5 = 676
    n = 20
    m = 60
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            close = v.get_series('close')
            em1 = v.ema(m1, close)
            em2 = v.ema(m2, close)
            em3 = v.ema(m3, close)
            em4 = v.ema(m4, close)
            em5 = v.ema(m5, close)
            sdv = (em2 + em3) / 2
            qsv = (em4 + em5) / 2
            vegas = (qsv > v.ref(1, qsv)) & (close > sdv) & (em1 > sdv)
            inc = close - v.ref(1, close)
            vol = v.get_series('volume')
            c1 = v.count((inc > 0) & (vol > v.ref(1, vol)), n) / v.count(inc > 0, n)
            c2 = v.count((inc <= 0) & (vol < v.ref(1, vol)), n) / v.count(inc <= 0, n)
            power_up = (c1 + c2 > 1) & (v.min(c1, c2) > .6)
            cci = v.get_series('cci')
            cci_con = (cci < 100) & (cci - v.ref(1, cci) > 20) & (v.ref(1, cci) < 0)
            o = v.get_series('open')
            start = (em1 > v.ref(1, em1)) & v.between(em1, o, close)
            upup = 100 * v.count(inc > 0, m) / m > 49
            condition = vegas & ~v.ref(1, vegas) & power_up & cci_con & start & upup
            self.static[v.code] = condition
        if self.static[v.code][v.date] and v.market_value > 6000000000:
            self.li_buy.add(k)
