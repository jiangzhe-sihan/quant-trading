# NAME=半导体信号弹
# DESCRIPTION=提示半导体etf的操作机会


def func(self, k, v):
    ma5 = v.ma(5, 'close')
    ma10 = v.ma(10, 'close')
    offset = (v.close - ma10) / ma10
    if ma5 > ma10:
        if (
                (.061 > offset > .06 or .035 > offset > .034) and .008 > v.increase_day > -.004
        ) or ((.015 > offset > .01 or .009 > offset > .007) and (v.increase < .02 or v.increase > .021)) or \
                (.001 > offset > -.005 and v.increase > -.019):
            self.li_sell.add(k)
        elif .06 > offset > .045 and v.increase > .04 and v.increase_day > .055:
            self.li_sell.add(k)
        elif .028 > offset > .007:
            if -.003 > v.increase > -.006 and v.increase_day < -.003:
                self.li_buy.add(k)
            elif -.02 < v.increase < -.015 and -.013 < v.increase_day < -.01:
                self.li_sell.add(k)
        elif offset < -.029 and -.034 < v.increase < -.03 and v.increase_day < -.035:
            self.li_buy.add(k)
    else:
        his = v.interval_max(10, 'close')
        quota = (v.close - his) / his
        if quota < -.038:
            if offset < -.012:
                if -.028 < v.increase < -.024 and -.027 < v.increase_day < -.023:
                    self.li_buy.add(k)
                elif -.018 < v.increase < -.015 and -.016 < v.increase_day < -.01:
                    self.li_buy.add(k)
                elif -.035 < v.increase < -.03 < v.increase_day < -.029:
                    self.li_buy.add(k)
        if v.close > ma10 and .017 > v.increase > .014:
            self.li_sell.add(k)
        if offset < -.098 and -.073 < v.increase < -.064 and -.06 < v.increase_day < -.055:
            self.li_buy.add(k)
        elif offset < -.058 and -.014 < v.increase < -.004 and v.increase_day < -.005:
            self.li_buy.add(k)
        elif -.031 < offset < -.024 and -.03 < v.increase < -.02 and -.018 < v.increase_day < -.015:
            self.li_buy.add(k)
