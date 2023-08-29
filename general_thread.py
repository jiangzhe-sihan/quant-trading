import pickle
import re
import threading
from concurrent.futures import ProcessPoolExecutor
from os import path, mkdir, walk, remove

from framework import Market, Investor
import random
from configure import *
from backtest import run_backtest
import matplotlib.pyplot as plt


def download_data(chn: Script, pool: list[str],
                  date_info: tuple,
                  callback: FunctionType = None):
    return chn.func(pool, date_info[0], date_info[1], callback)


def write_data(pool: list[str],
               res: dict[str, list[dict[str, str | int | float]]],
               save_path: str,
               callback: FunctionType = None):
    if not path.exists(save_path):
        mkdir(save_path)
    for i in next(walk(save_path))[2]:
        if i == 'date_info.pkl':
            continue
        code = re.match(r'\[(.*?)[]]', i)
        if code:
            if code.group(1) not in pool:
                remove(save_path + i)
            else:
                if i[:-5] not in res:
                    remove(save_path + i)
        else:
            if i not in pool:
                remove(save_path + i)
    for k, v in res.items():
        if k == 'date_info':
            fp = open(save_path + 'date_info.pkl', 'wb+')
            pickle.dump(v, fp)
            fp.close()
            continue
        k = k.replace('*', '+')
        fp = open(save_path + k + '.json', 'w+')
        json.dump(v, fp)
        fp.close()
        if callback is not None:
            ret = callback()
            if ret != 0:
                raise SystemError('write aborted.')


class ProgressCalc:
    def __init__(self, length: int):
        self._total = length
        self._count = 0
        self._progress = 0

    def get_progress(self, current: int, length: int):
        if current == self._count and length == self._total:
            return self._progress
        self._count = current
        self._total = length
        self._progress = self._count / self._total
        return self._progress


class ProgressThread(threading.Thread):
    def __init__(self, func, args: tuple = None, kw: dict = None,
                 length: int = 200, callback=None):
        super().__init__()
        self._func = func
        self._args = args if args is not None else ()
        self._kw = kw if kw is not None else {}
        self._count = 0
        self._total = length
        self._callback = callback
        self._calc = ProgressCalc(length)
        self.res = None
        self.exception = None
        self.code = 0
        self.msg = None
        self.daemon = True
        self.finished = threading.Event()

    @property
    def progress(self):
        return self._calc.get_progress(self._count, self._total)

    def set_callback(self, func):
        self._callback = func

    def step(self):
        self._count += 1

    def cancel(self):
        self.finished.set()

    def run(self):
        try:
            self.finished.wait(.01)
            if not self.finished.is_set():
                self.res = self._func(*self._args, **self._kw, callback=self._callback)
        except Exception as e:
            self.exception = e
            self.code = 1
        finally:
            self.finished.set()


class CallbackFactory:
    @staticmethod
    def get_instance(obj: ProgressThread, add_func=None):
        if add_func is not None:
            def func():
                obj.step()
                add_func()
                if obj.finished.is_set():
                    return 1
                return 0
        else:
            def func():
                obj.step()
                if obj.finished.is_set():
                    return 1
                return 0
        return func


class MarketDownloader(ProgressThread):
    """股票数据下载线程"""
    def __init__(self, chn: Script, pool: list[str], date_info: tuple):
        super().__init__(download_data, args=(chn, pool, date_info), length=len(pool))


class MarketWriter(ProgressThread):
    """股票数据写入线程"""
    def __init__(self, pool: list[str], res: dict[str, list[dict[str, str | int | float]]], save_path: str):
        super().__init__(write_data, args=(pool, res, save_path), length=len(pool))


class MarkerLoader(ProgressThread):
    """股票数据加载进程"""
    def __init__(self, market: Market, src: str | dict[str, list[dict[str, str | int | float]]],
                 prop: list[tuple[str, FunctionType]] = None):
        super().__init__(market.load, args=(src, prop))
        self._market = market

    @property
    def progress(self):
        return self._calc.get_progress(self._count, self._market.len)


class BacktestThread(ProgressThread):
    """回测进程"""
    def __init__(self, player: Investor, li_stg: list[FunctionType]):
        super().__init__(run_backtest, args=(player, li_stg))
        self._market = player.market

    @property
    def progress(self):
        return self._calc.get_progress(self._count, len(self._market))


class MarketSliceProcessor(ProgressThread):
    def __init__(self, market: Market, group_buy, group_sell):
        super().__init__(self._func, callback=CallbackFactory.get_instance(self))
        self._market = market
        self._group_buy = group_buy
        self._group_sell = group_sell

    def _func(self, callback):
        self._total = len(self._market.slices)
        args = []
        for i in self._market.slices:
            args.append((i, self._group_buy, self._group_sell))
        with ProcessPoolExecutor() as executor:
            res = {}
            for i in executor.map(vec_filter, args):
                res.update(i)
                self.step()
        return res


class MultiThreadLoader(ProgressThread):
    """多重线程加载线程"""
    def __init__(self, tds: list[ProgressThread]):
        super().__init__(self._func, callback=CallbackFactory.get_instance(self))
        self._tds = tds

    def _func(self, callback):
        self._total = len(self._tds)
        random.shuffle(self._tds)
        for td in self._tds:
            td.set_callback(CallbackFactory.get_instance(td, lambda: self.step()))
            td.start()
        for td in self._tds:
            td.join()
        return [td.res for td in self._tds]


class PlotThread:
    @staticmethod
    def update():
        plt.show()
