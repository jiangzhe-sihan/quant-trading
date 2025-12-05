# NAME=条件单
# DESCRIPTION=固定百分比止盈


def func(self):
    # 止盈幅度
    stop_income_pct = .02
    # 止损幅度
    stop_lose_pct = -.02
    for k, v in self.warehouse.items():
        if v.income_pct > stop_income_pct or v.income_pct < stop_lose_pct:
            self.li_sell.add(k)
