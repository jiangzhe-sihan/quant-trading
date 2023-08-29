# NAME=魔改十字星
# DESCRIPTION=十字星筛选策略·改

def func(self):
    """十字星筛选策略·改"""
    for k, v in self.market.tell.items():
        va5 = v.ma(5, 'volume')
        increase = v.increase
        increase_day = v.increase_day
        if (v.volume - va5) / va5 > .14:
            up = increase_day - v.low_offset
            down = v.high_offset - increase_day
            if increase > .008 and up > down and up > .038:
                self.li_sell.add(k)
            if increase < -.018 and down > up and down > .046:
                if increase_day < -.102:
                    self.li_sell.add(k)
                else:
                    self.li_buy.add(k)
        elif (v.volume - va5) / va5 < -.14:
            up = increase_day - v.low_offset
            down = v.high_offset - increase_day
            up, down = down, up
            if increase_day > -.001 and up > down:
                self.li_sell.add(k)
            elif abs(increase_day) < .004:
                if increase_day > 0:
                    up = v.high_offset - increase_day
                    down = -v.low_offset
                else:
                    up = v.high_offset
                    down = increase_day - v.low_offset
                if up > .033:
                    self.li_buy.add(k)
                if down > .017:
                    self.li_sell.add(k)
