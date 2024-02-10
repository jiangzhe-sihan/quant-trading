# NAME=纳斯达克信号弹
# DESCRIPTION=提示纳指etf的操作机会

def func(self, k, v):
    if -.00 < v.increase_day < .002 and v.increase < -.024:
        self.li_buy.add(k)
    ma5 = v.ma(5, 'close')
    ma10 = v.ma(10, 'close')
    if -.001 < (v.close - ma5) / ma5 < .006 and -.003 < v.increase_day < -.00 and -.008 < v.increase < -.006:
        self.li_buy.add(k)
    if ma5 > ma10:
        his = v.interval_min(10, 'close')
        quota = (v.close - his) / his
        if quota > .084 or .07 > quota > .048:
            if v.close > ma5:
                if -.004 < v.increase_day < -.002 and (v.increase > -.001 or -.003 > v.increase):
                    self.li_sell.add(k)
                if .018 < v.increase < .019 and .038 < (v.close - ma10) / ma10 < .039:
                    self.li_sell.add(k)
                    self.li_sell.add(k)
                if .004 < v.increase_day < .007 and .013 < v.increase < .015:
                    self.li_sell.add(k)
            if .006 > (v.close - ma10) / ma10 > .005 and -.028 < v.increase < 0:
                self.li_buy.add(k)
        elif .025 > quota > .018:
            if .012 > v.increase > .01 and .013 > (v.close - ma10) / ma10 > .011:
                self.li_sell.add(k)
        elif .017 > quota > .012:
            if -.003 > (v.close - ma10) / ma10 > -.004:
                self.li_buy.add(k)
        if (v.close - ma10) / ma10 > .103:
            self.li_sell.add(k)
    else:
        his = v.interval_max(10, 'close')
        quota = (v.close - his) / his
        if quota < -.092 or -.081 < quota < -.065 or -.063 < quota < -.059 or -.058 < quota < -.054:
            if -.004 < v.increase_day < -.0012 or (-.039 < v.increase < -.03 or -.029 < v.increase < -.028):
                if not (self.market.date_handler.month == 12 and self.market.date_handler.day):
                    self.li_buy.add(k)
            elif v.increase_day > v.increase > .024:
                self.li_sell.add(k)
            if v.close > ma5 and (.01 > v.increase_day > -.006 or v.increase > .033):
                self.li_sell.add(k)
            if -.049 < (v.close - ma10) / ma10 < -.042 and (
                    -.025 < v.increase < -.021) and -.013 < v.increase_day < -.008:
                self.li_buy.add(k)
            if -.014 < (v.close - ma10) / ma10 < -.012:
                self.li_buy.add(k)
        elif -.042 < quota < -.037:
            if -.024 < (v.close - ma10) / ma10 < -.023:
                self.li_buy.add(k)
        if (
            (v.close - ma10) / ma10 < -.09 or -.08 < (v.close - ma10) / ma10 < -.059
            ):
            self.li_buy.add(k)
        elif (v.close - ma10) / ma10 > .031 and v.increase > .056 and -.005 < v.increase_day < .002:
            self.li_sell.add(k)
