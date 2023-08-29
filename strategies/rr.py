# NAME=轮转
# DESCRIPTION=大小盘轮动，但是轮一群~

def func(self):
    """轮转策略"""
    li = []
    for k, v in self.market.tell.items():
        his = v.get_history_value(6, 'close')
        quota = (v.close - his) / his
        li.append((k, v, quota))
    if not li:
        return
    li.sort(key=lambda x: x[2], reverse=True)
    best = li[-1] if len(li) == 1 else li[-2]
    if best[2] < -.09:
        self.li_buy.add(best[0])
        for k in self.market.tell:
            if k == best[0]:
                continue
            self.li_sell.add(k)
    else:
        best = li[len(li) // 3 - 1]
        if best[2] > .1:
            self.li_buy.add(best[0])
            for k in self.market.tell:
                if k == best[0]:
                    continue
                self.li_sell.add(k)
        else:
            for k in self.market.tell:
                self.li_sell.add(k)
