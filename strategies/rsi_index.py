# NAME=rsi指标
# DESCRIPTION=参考rsi指标进行决策

prop = [
    ('high', lambda x: x.high)
]

def func(self):
    for k, v in self.market.tell.items():
        r1, r2, r3 = v.rsi_group()
        r1 *= .01
        r2 *= .01
        r3 *= .01
        std = 2 * r2 - r3 + v.increase
        if r1 <= r2 <= r3:
            if r1 < std and r1 < .3 or r1 < .2:
                self.li_buy.add(k)
        elif r1 >= r2 >= r3:
            if r1 > std and r1 > .8 or r1 > .9:
                self.li_sell.add(k)
