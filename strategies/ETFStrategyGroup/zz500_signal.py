# NAME=中证500信号弹
# DESCRIPTION=提示中证500etf的操作机会

def func(self, k, v):
    ma5 = v.ma(5, 'close')
    ma10 = v.ma(10, 'close')
    if ma5 > ma10:
        if (v.high - ma10) / ma10 > .014 and -.007 < (v.close - ma5) / ma5 < -.003:
            if -.01 < v.increase < -.007 and -.008 < v.increase_day < -.007:
                self.li_buy.add(k)
        if (v.close - ma10) / ma10 > .07 and .01 < v.increase < .03 and .01 < v.increase_day < .018:
            self.li_sell.add(k)
        elif (v.close - ma10) / ma10 > .032 and .005 < v.increase < .007 and .004 < v.increase_day < .008:
            self.li_sell.add(k)
        elif (v.close - ma10) / ma10 > .029 and .018 < v.increase < .03 and \
                (.01 < v.increase_day < .016 or .017 < v.increase_day < .018):
            self.li_sell.add(k)
        elif (v.close - ma10) / ma10 > .017 and (
                .001 < v.increase < .006 or .015 < v.increase < .033
        ) and (-.002 < v.increase_day < .002 or .007 < v.increase_day < .018):
            self.li_sell.add(k)
        elif (v.close - ma10) / ma10 > .01:
            if .009 < v.increase < .015 and -.002 < v.increase_day < .007:
                self.li_sell.add(k)
            elif v.increase < -.015 and -.021 < v.increase_day < -.015:
                self.li_buy.add(k)
        elif .01 > (v.close - ma10) / ma10 > .003 and -.012 < v.increase < -.003 and -.002 < v.increase_day < .005:
            self.li_buy.add(k)
        elif (v.close - ma10) / ma10 > -.01 and -.044 < v.increase < -.033 and -.046 < v.increase_day < -.035:
            self.li_buy.add(k)
        elif (v.close - ma10) / ma10 > -.019 and -.025 < v.increase < -.02 and -.021 < v.increase_day < -.013:
            self.li_buy.add(k)
    else:
        his = v.interval_max(10, 'close')
        quota = (v.close - his) / his
        if quota < -.055:
            if -.04 < (v.close - ma10) / ma10 < -.033 and -.016 < v.increase < -.005 and -.015 < v.increase_day < -.011:
                self.li_buy.add(k)
            elif (v.close - ma10) / ma10 < -.048 and -.03 < v.increase < -.022 and -.019 < v.increase_day < -.015:
                self.li_buy.add(k)
        elif quota < -.042:
            if -.028 < (v.close - ma10) / ma10 < -.024:
                if -.01 < v.increase < -.005 and -.008 < v.increase_day < -.00:
                    self.li_buy.add(k)
                elif -.05 < v.increase < -.005 and -.038 < v.increase_day < -.019:
                    self.li_buy.add(k)
        elif quota < -.038:
            if v.increase < -.004 and -.005 < v.increase_day < -.002:
                self.li_buy.add(k)
            if (v.close - ma10) / ma10 < -.03:
                self.li_buy.add(k)
        if (v.close - ma10) / ma10 < -.1 and v.increase < -.08 and -.01 < v.increase_day < 0:
            self.li_buy.add(k)
        elif ((v.close - ma10) / ma10 < -.064 or -.039 < (v.close - ma10) / ma10 < -.035) and \
                -.03 < v.increase < -.022 and -.025 < v.increase_day < -.02:
            self.li_buy.add(k)
        elif (v.close - ma10) / ma10 < -.02 and v.increase < -.035 and -.025 < v.increase_day < 0:
            self.li_buy.add(k)
        elif -.01 < (v.close - ma10) / ma10 < .0 and .013 < v.increase < .015:
            self.li_sell.add(k)
        elif (v.close - ma10) / ma10 < -.002 and .001 < v.increase < .005 and -.005 < v.increase_day < -.00:
            self.li_buy.add(k)
        elif .05 > (v.close - ma10) / ma10 > .007 and .016 < v.increase < .02 and .015 < v.increase_day < .02:
            self.li_sell.add(k)
