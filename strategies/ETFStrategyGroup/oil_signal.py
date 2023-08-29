# NAME=原油信号弹
# DESCRIPTION=提示原油etf的操作机会


def func(self, k, v):
    ma5 = v.ma(5, 'close')
    ma10 = v.ma(10, 'close')
    if ma5 > ma10:
        if .00 < v.increase_day < .001 and v.increase > .014:
            self.li_sell.add(k)
        if .04 < (v.close - ma10) / ma10 < .055:
            if .018 > v.increase > .015 and v.increase_day > .008:
                self.li_sell.add(k)
            elif .008 < v.increase < .017 and v.increase_day < -.02:
                self.li_sell.add(k)
        if .041 < (v.high - ma10) / ma10 < .055 and .006 > v.increase and v.increase_day > .005:
            self.li_sell.add(k)
        if (v.close - ma10) / ma10 > .064:
            self.li_sell.add(k)
        if (v.close - ma5) / ma5 < -.034 and \
                (v.increase < -.035 or -.028 < v.increase < -.02) and \
                -.015 < v.increase_day < -.005:
            self.li_buy.add(k)
    else:
        his = v.interval_max(10, 'close')
        quota = (v.close - his) / his
        if (
            quota < -.093 or -.085 < quota < -.06 or -.058 < quota < -.057 or
            -.056 < quota < -.052 or -.041 < quota < -.039
        ):
            if v.close < ma5:
                if (
                    -.0164 < v.increase_day < -.0159 or -.015 < v.increase_day < -.012 or
                    -.01 < v.increase_day < -.008 or -.007 < v.increase_day < -.006 or
                    -.049 < v.increase < -.035 or -.007 < v.increase < -.006
                ):
                    if not (
                        (self.market.date_handler.month == 11) or
                        (self.market.date_handler.month == 12 and 20 < self.market.date_handler.day < 24)
                    ):
                        self.li_buy.add(k)
                elif v.increase_day > v.increase > .028:
                    self.li_sell.add(k)
            else:
                if .006 > v.increase_day > .004 or v.increase > .018:
                    self.li_sell.add(k)
                elif .00 < v.increase_day < .001:
                    self.li_buy.add(k)
        if (v.close - ma10) / ma10 < -.053 and -.001 < v.increase_day < .003:
            if not (
                (self.market.date_handler.month == 11 and 10 < self.market.date_handler.day < 20) or
                (self.market.date_handler.month == 12 and 20 < self.market.date_handler.day)
            ):
                self.li_buy.add(k)
