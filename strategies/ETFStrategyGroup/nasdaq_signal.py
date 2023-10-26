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
        if quota > .048:
            if -.004 < v.increase_day < -.002 and v.close > ma5:
                self.li_sell.add(k)
        if (v.close - ma10) / ma10 > .103:
            self.li_sell.add(k)
    else:
        his = v.interval_max(10, 'close')
        quota = (v.close - his) / his
        if quota < -.092 or -.081 < quota < -.065 or -.063 < quota < -.054:
            if -.004 < v.increase_day < -.001 or -.039 < v.increase < -.028:
                if not (self.market.date_handler.month == 12 and self.market.date_handler.day):
                    self.li_buy.add(k)
            elif v.increase_day > v.increase > .024:
                self.li_sell.add(k)
            if v.close > ma5 and (.01 > v.increase_day > -.006 or v.increase > .033):
                self.li_sell.add(k)
            if -.049 < (v.close - ma10) / ma10 < -.042 and (
                    -.025 < v.increase < -.021) and -.013 < v.increase_day < -.008:
                self.li_buy.add(k)
        if (v.close - ma10) / ma10 < -.09 or -.08 < (v.close - ma10) / ma10 < -.059:
            self.li_buy.add(k)
        elif (v.close - ma10) / ma10 > .031 and v.increase > .056 and -.005 < v.increase_day < .002:
            self.li_sell.add(k)