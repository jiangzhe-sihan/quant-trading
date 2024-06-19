# NAME=轮转
# DESCRIPTION=大小盘轮动，但是轮一群~

prop = [
    ('成交额', lambda x: x.amount),
    ('换手', lambda x: x.hs),
    ('量比', lambda x: x.lb),
    ('涨停', lambda x: x.daily_limit),
    ('跌停', lambda x: x.limit_down), 
    ('index', lambda x: x.hs * x.lb),
    ('ma_deincr', lambda x: 60 * x.ma(60, lambda x: x.increase if x.increase <= 0 else 0) / x.count(lambda x: x.increase <= 0, 60))
]


def func(self):
    """轮转策略"""
    li = []
    for k, v in self.market.tell.items():
        his = v.interval_max(7, 'close')
        quota = (v.close - his) / his
        li.append((k, v, quota))
    if not li:
        return
    li.sort(key=lambda x: x[2], reverse=True)
    num = 2
    best = li[0] if len(li) < num else li[-num]
    hs = best[1].hs
    idx = hs * best[1].lb
    if best[2] < -.102 and (
            ((idx > 8.2 or 6.3 > idx > .25) and 14.15 > hs > .2) or 
            (.09 > idx > .05 and .05 < hs < .12)
        ) and best[1].close > 1.2:
        self.li_buy.add(best[0])
    else:
        best = li[len(li) // 3 - 1]
        if best[2] > .1:
            self.li_buy.add(best[0])
    self.clear()
