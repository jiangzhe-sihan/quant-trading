# NAME=房地产信号弹
# DESCRIPTION=提示房地产etf的操作机会


def func(self, k, v):
    ma5 = v.ma(5, 'close')
    ma10 = v.ma(10, 'close')
    if ma5 > ma10:
        if (v.close - ma10) / ma10 > .042 and .02 > v.increase > .014 and .016 > v.increase_day > .0:
            self.li_sell.add(k)
        elif (v.close - ma10) / ma10 > .037 and -.002 < v.increase < .005 and .012 < v.increase_day < .035:
            self.li_sell.add(k)
        elif (v.close - ma10) / ma10 > .032 and .00 < v.increase < .008 and .0 < v.increase_day < .005:
            self.li_sell.add(k)
        elif (v.close - ma10) / ma10 > .025 and -.001 < v.increase < .001 and -.002 < v.increase_day < .001:
            self.li_sell.add(k)
        elif (v.close - ma10) / ma10 > .014 and .01 < v.increase < .013 and v.increase_day > .005:
            self.li_sell.add(k)
        elif (v.close - ma10) / ma10 < -.006 and -.014 < v.increase < -.008 and -.009 < v.increase_day < -.006:
            self.li_buy.add(k)
    else:
        his = v.interval_max(10, 'close')
        quota = (v.close - his) / his
        if quota < -.064:
            if v.increase < -.07 or -.061 < v.increase < -.051:
                self.li_buy.add(k)
            if -.077 < (v.close - ma10) / ma10 < -.068 and (
                    -.009 < v.increase < -.007 or -.035 < v.increase < -.025
            ) and (
                    -.008 < v.increase_day < -.005 or -.025 < v.increase_day < -.016
            ):
                self.li_buy.add(k)
        if (v.close - ma10) / ma10 < -.048 and -.024 < v.increase < -.017 and -.025 < v.increase_day < -.015:
            self.li_buy.add(k)
        elif -.03 < (v.close - ma10) / ma10 < -.025 and -.029 < v.increase < -.026 and -.024 < v.increase_day < -.018:
            self.li_buy.add(k)
        elif -.024 < (v.close - ma10) / ma10 < -.021 and -.012 < v.increase < -.006 and -.013 < v.increase_day < -.008:
            self.li_buy.add(k)
        elif -.01 < (v.close - ma10) / ma10 < .00 and .023 < v.increase < .03 and .02 < v.increase_day < .025:
            self.li_sell.add(k)
        elif .001 < (v.close - ma10) / ma10 < .005 and (
                .037 < v.increase < .041 and .035 < v.increase_day < .038):
            self.li_sell.add(k)
        elif .021 < (v.close - ma10) / ma10 < .025 and (
                .045 < v.increase < .055 and .045 < v.increase_day < .052):
            self.li_sell.add(k)
