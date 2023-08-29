# NAME=美股下跌中继
# DESCRIPTION=在美股的下跌中继做反弹

def func(self):
    """下跌中继做反弹"""
    for k, v in self.market.tell.items():
        ma5 = v.ma(5, 'close')
        ma10 = v.ma(10, 'close')
        if ma5 > ma10:
            pass
        his = v.interval_max(10, 'close')
        quota = (v.close - his) / his
        if quota < -.04 or -.03 < quota < -.025:
            if v.increase < -.027 and v.open < ma5:
                self.li_buy.add(k)
            elif v.close > ma5 or v.high > ma10:
                self.li_sell.add(k)
