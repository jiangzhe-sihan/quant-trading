# NAME=条件单
# DESCRIPTION=动态百分比止盈


def func(self):
    # 触发止盈监测幅度
    trigger_pct = .05
    # 回调止盈幅度
    drawdown_pct = -.04
    # 止损幅度
    stop_lose_pct = -.02
    for k, v in self.warehouse.items():
        if v.income_pct < stop_lose_pct or (v.max_income_pct > trigger_pct and v.income_pct / v.max_income_pct - 1 < drawdown_pct):
            self.li_sell.add(k)
