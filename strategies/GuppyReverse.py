# NAME=GuppyReverse
# DESCRIPTION=顾比倒计时（反弹版）


prop = [
    ('换手', lambda x: f'{x.hs} %'),
    ('量比', lambda x: x.lb),
    ('市值', lambda x: f'{x.market_value / 10000:.2f} 亿'),
    ('lwr1', lambda x: x.lwr()[0]),
    ('lwr2', lambda x: x.lwr()[1]),
    ('成交额（模拟）', lambda x: x.volume * (x.open + x.close) * 50),
    ('5日平均成交额', lambda x: x.ma(5, 'amount')),
    ('ma5', lambda x: x.ma(5, 'close')),
    ('ema5', lambda x: x.ema(5, 'close')),
    ('sma5', lambda x: x.sma(5, 1, 'close'))
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    self.static['bottom'] = self.static.get('bottom', {})
    self.static['top'] = self.static.get('top', {})
    self.static['buys'] = self.static.get('buys', set())
    self.static['sells'] = self.static.get('sells', set())
    interval = 5
    count = 3
    for k, v in self.market.tell.items():
        lwr1, lwr2 = v.lwr()
        self.static['bottom'][k] = self.static['bottom'].get(k, None)
        self.static['top'][k] = self.static['top'].get(k, None)
        buys = self.static.get('buys')
        sells = self.static.get('sells')
        amount = (v.open + v.close) * v.volume / 2
        # 更新压力位
        if v.previous and v.interval_min(interval, 'low') == v.previous.low and v.low > v.previous.low:
            pls = [v.get_history_value(1, 'high')]
            for i in range(2, interval + 1):
                p_high = v.get_history_value(i, 'high')
                if p_high > pls[-1]:
                    pls.append(p_high)
                if (len(pls) > 1 and pls[-1] / pls[-2] - 1 > .053) or (len(pls) == 1 and pls[0] / v.close - 1 > .013):
                    for _ in range(count):
                        pls.insert(0, None)
                if len(pls) >= count:
                    # pls.append((v.get_history_value(i, 'high') + v.get_history_value(i, 'low')) / 2)
                    if self.static['bottom'][k] and self.static['bottom'][k] > pls[-1]:
                        buys.remove(k) if k in buys else None
                    self.static['bottom'][k] = pls[-1]
                    break
        # 更新支撑位
        if v.previous and v.interval_max(interval, 'high') == v.previous.high and v.high < v.previous.high:
            sls = [v.get_history_value(1, 'high')]
            for i in range(2, interval + 1):
                p_low = v.get_history_value(i, 'high')
                if p_low < sls[-1]:
                    sls.append(p_low)
                if len(sls) >= count:
                    # self.static['top'][k] = sls[-1]
                    break
            self.static['top'][k] = sls[-1]
        # 突破买入
        bottom = self.static['bottom'][k]
        if bottom is not None and v.close > bottom:
            if (k not in buys and v.interval_min(count, 'low') != v.low and 
                    lwr1 > lwr2 > 60 and ((v.lb > 1.3 and v.hs < 20) or 3 < v.hs < 19) and 
                    (v.close > 12 or v.close < 3) and 
                    (amount > 560000 or v.ma(5, 'amount') > 60000000)
                ):
                self.li_buy.add(k)
                buys.add(k)
                sells.remove(k) if k in sells else None
                # self.static['bottom'][k] = None
                continue
        # 跌破卖出
        top = self.static['top'][k]
        if top is not None and v.close < top:
            if k not in sells:
                self.li_sell.add(k)
                sells.add(k)
                buys.remove(k) if k in buys else None
                self.static['top'][k] = None
