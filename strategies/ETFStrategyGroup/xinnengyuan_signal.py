# NAME=新能源信号弹
# DESCRIPTION=提示新能源etf的操作机会


def func(self, k, v):
    ma5 = v.ma(5, 'close')
    ma10 = v.ma(10, 'close')
    if ma5 > ma10:
        if v.close > ma5 and (
            v.increase_day > .05 or .04 > v.increase_day
        ) and v.increase > .026:
            self.li_sell.add(k)
        if v.close < ma5 and -.009 < v.increase < -.006:
            self.li_buy.add(k)
        if .023 < (v.close - ma10) / ma10 < .034 and -.028 < v.increase < -.018 and -.015 < v.increase_day < -.01:
            self.li_buy.add(k)
    else:
        his = v.interval_max(10, 'high')
        quota = (v.close - his) / his
        if quota < -.073 or -.069 < quota < -.06:
            if v.close < ma5:
                if -.025 < v.increase_day < -.02 and v.increase < -.024:
                    self.li_buy.add(k)
                elif -.024 < v.increase_day < -.011 and -.016 < v.increase < -.01:
                    self.li_buy.add(k)
                elif -.014 < v.increase_day < -.006 and -.016 < v.increase < -.01:
                    self.li_buy.add(k)
            elif v.close > ma10:
                if v.increase_day < 0 or v.increase < -.005:
                    self.li_buy.add(k)
        if v.close > ma10 and v.increase > .0 and v.increase_day > .02:
            self.li_sell.add(k)
        if (v.close - ma10) / ma10 < -.059 and -.04 < v.increase < -.02:
            self.li_buy.add(k)
        if v.close > ma5 and .003 < v.increase_day < v.increase < .005:
            self.li_buy.add(k)
