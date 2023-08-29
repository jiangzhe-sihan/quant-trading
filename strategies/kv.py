# NAME=kv
# DESCRIPTION=k线成交量筛选策略

def func(self):
    """k线成交量筛选策略"""
    for k, v in self.market.tell.items():
        va5 = v.ma(5, 'volume')
        va10 = v.ma(10, 'volume')
        increase = v.increase
        increase_day = v.increase_day
        if increase_day < 0:
            down_shadow = increase_day - v.low_offset
            up_shadow = v.high_offset
        else:
            down_shadow = -v.low_offset
            up_shadow = v.high_offset - increase_day
        if va5 > va10:
            bottom = va10
            top = va5
        else:
            bottom = va5
            top = va10
        if (top - bottom) / top < .03 and increase_day > 0 and abs((v.volume - bottom) / bottom) < .2:
            down_shadow = -v.low_offset
            if down_shadow > .025:
                self.li_buy.add(k)
        if abs((v.volume - bottom) / bottom) < .02:
            if increase < -.012 and increase_day > .021:
                self.li_buy.add(k)
        if abs((v.volume - bottom) / bottom) < .03:
            if increase > .03 > increase_day and down_shadow > .033:
                self.li_sell.add(k)
            if increase_day < -.042:
                self.li_buy.add(k)
        if abs((v.volume - bottom) / bottom) < .18:
            if increase_day > increase and .031 < increase_day < .048:
                self.li_buy.add(k)
            if increase_day > .065:
                self.li_sell.add(k)
        if abs((v.volume - bottom) / bottom) < .37:
            if down_shadow > .033:
                self.li_buy.add(k)
        if abs((v.volume - top) / top) < .26:
            if up_shadow > .04:
                self.li_sell.add(k)
