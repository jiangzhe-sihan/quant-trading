# NAME=美元债信号弹
# DESCRIPTION=提示美元债etf的操作机会

def func(self, k, v):
    ma5 = v.ma(5, 'close')
    ma10 = v.ma(10, 'close')
    offset = (v.close - ma10) / ma10
    if ma5 > ma10:
        if .027 > offset > .014 and \
                (.02 > v.increase > .006) and \
                (.021 > v.increase_day > .011 or .009 > v.increase_day > .0):
            self.li_sell.add(k)
        elif offset > .13:
            self.li_sell.add(k)
        if -.008 < offset < -.006 and -.012 < v.increase < -.007 and -.008 < v.increase_day < -.002:
            self.li_buy.add(k)
        elif .002 > offset > .00 and -.003 < v.increase < -.002 and -.003 < v.increase_day < -.002:
            self.li_buy.add(k)
        elif .01 > offset > .006 and -.015 < v.increase < -.01 and -.02 < v.increase_day < -.01:
            self.li_buy.add(k)
    else:
        his = v.interval_max(10, 'close')
        quota = (v.close - his) / his
        if quota < -.052:
            if v.increase < -.014 and -.006 < v.increase_day < -.002:
                self.li_buy.add(k)
        if .008 < offset < .01 and .008 < v.increase < .011 and .008 < v.increase_day < .011:
            self.li_sell.add(k)
        elif -.009 < offset < -.007 and -.004 < v.increase_day < -.002 and -.004 < v.increase < -.002:
            self.li_buy.add(k)
        elif -.005 < offset < -.004 and -.003 < v.increase_day < -.002 and -.007 < v.increase < -.004:
            self.li_buy.add(k)
        elif -.03 < offset < -.01 and \
                (-.025 < v.increase < -.02 or -.006 < v.increase < .00) and \
                (v.increase_day < -.022 or -.001 < v.increase_day < .001):
            self.li_buy.add(k)
