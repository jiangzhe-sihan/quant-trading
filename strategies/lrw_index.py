# NAME=lrw_index
# DESCRIPTION=LWR指标，死叉买入，金叉卖出。


prop = []


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    for k, v in self.market.tell.items():
        lwr1, lwr2 = v.lwr()
        plwr1, plwr2 = v.get_history_value(1, 'lwr')
        if plwr1 and plwr2:
            if plwr1 > plwr2 and 93 < lwr1 < lwr2:
                self.li_buy.add(k)
            elif plwr1 < plwr2 and lwr1 > lwr2:
                self.li_sell.add(k)
