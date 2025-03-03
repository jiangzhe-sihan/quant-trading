from typing import Iterable

import matplotlib.pyplot as plt
from types import FunctionType
from framework import Investor


def run_backtest(investor: Investor, strategies: Iterable, callback: FunctionType = None):
    """运行回测"""
    while True:
        for f in strategies:
            f(investor)
        if not investor.update():
            break
        if callback is not None:
            ret = callback()
            if ret != 0:
                raise SystemError('backtest aborted.')
    investor.settle()


def draw_warehouse_income(self: Investor):
    """绘制持仓收益率曲线"""
    fig = plt.figure('持仓收益率')
    plt.grid(linestyle='-.')
    plt.plot(self.history_date, self.history_floating)
    plt.axhline(c='orange')
    return fig


def draw_grant_income(self: Investor):
    """绘制累计收益率曲线"""
    fig = plt.figure('累计收益率')
    plt.grid(linestyle='-.')
    plt.plot(self.history_date, self.history_income_rate)
    return fig


def draw_unit_worth(self: Investor):
    """绘制单位净值曲线"""
    fig = plt.figure('单位净值')
    plt.grid(linestyle='-.')
    plt.plot(self.history_date, self.history_value)
    return fig


def print_strategy_history(self: Investor):
    """打印历史策略记录"""
    for k, v in self.strategy_history.items():
        print(k)
        print(v)
