# NAME=动态切换
# DESCRIPTION=判断行情阶段并动态切换策略

def func(self):
    for k, v in self.market.tell.items():
        short_low = v.interval_min(16, 'low')
        short_high = v.interval_max(16, 'high')
        long_low = v.interval_min(40, 'low')
        long_high = v.interval_max(40, 'high')
        if long_high != long_low:
            if .98 < abs((short_high - short_low) / (long_high - long_low)) < 1.02:
                if v.close / long_low < 1.02:
                    self.li_buy.add(k)
                elif v.open / short_high > .98:
                    self.li_sell.add(k)
                continue
        ma5 = v.ma(5, 'close')
        ma10 = v.ma(10, 'close')
        va5 = v.ma(5, 'volume')
        if ma5 > ma10:
            his = v.interval_min(20, 'low')
            quota = (v.close - his) / his
            if quota > .01:
                if v.volume / va5 > 1.25 and v.increase < -.025 and (v.close < ma5 or v.low < ma10):
                    self.li_buy.add(k)
                elif v.volume / va5 > .72 and (v.increase > -.012 or v.close < ma5):
                    self.li_sell.add(k)
                elif v.volume / va5 < .64 and v.increase > .01:
                    self.li_sell.add(k)
        else:
            if short_low == v.close and (v.close - short_high) / short_high < -.075:
                if v.volume / va5 > 1.5:
                    self.li_sell.add(k)
            if v.volume / va5 > .96 and v.close > ma10:
                self.li_sell.add(k)
