# NAME=英维克
# DESCRIPTION=提示英维克的操作机会


def func(self, k, v):
    width = v.close / v.low - 1
    ma5 = v.ma(5, 'close')
    ma10 = v.ma(10, 'close')
    bia10 = v.close / ma10 - 1
    his1 = v.interval_max(10, 'close')
    bia_max_10 = v.close / his1 - 1
    his2 = v.interval_min(10, 'close')
    bia_min_10 = v.close / his2 - 1
    bia_mid_10 = abs(bia_max_10 + bia_min_10)
    if ma5 > ma10:
        if bia_max_10 < -.184:
            if v.increase < v.increase_day < -.045 and bia10 < -.093:
                self.li_buy.add(k)
            if v.increase < -.1 and abs(v.increase_day) < .001 and bia10 < -.052:
                self.li_buy.add(k)
    else:
        if bia_max_10 < -.272:
            if v.increase < v.increase_day < -.054 and bia10 < -.173:
                self.li_buy.add(k)
        elif bia_max_10 < -.225:
            if v.increase < v.increase_day < -.022 and -.113 < bia10 < -.081:
                self.li_buy.add(k)
        elif bia_max_10 < -.125:
            if -.026 < v.increase_day < v.increase < -.011 and -.12 < bia10 < -.06:
                self.li_buy.add(k)
            if -.009 < v.increase < v.increase_day < -.006 and bia10 < -.09:
                self.li_buy.add(k)
            if v.increase < v.increase_day < -.008 and abs(v.increase_day + width) < .005 and -.092 < bia10 < -.061:
                self.li_buy.add(k)
            if v.increase < 0 < v.increase_day < .011 and abs(v.increase + width) < .006 and bia10 < -.081:
                self.li_buy.add(k)
            if -.049 < v.increase < v.increase_day < -.037 and bia10 < -.084:
                self.li_buy.add(k)
            if v.increase < 0 < v.increase_day < .046 and bia10 < -.1:
                self.li_buy.add(k)
        elif bia_max_10 < -.101:
            if -.018 < v.increase_day < v.increase < -.012 and bia10 < -.06:
                self.li_buy.add(k)
            if v.increase < v.increase_day < -.037 and -.071 < bia10 < -.034:
                self.li_buy.add(k)
        if bia_mid_10 < .012:
            if width > .04 > v.increase_day > .025 and abs(bia10) < .005:
                self.li_buy.add(k)
