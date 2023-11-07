from __future__ import annotations

import os
import sys
from math import ceil
from os import walk
from types import FunctionType
import json
import pandas as pd
import numpy as np
import datetime

from vector import Vector


class Date:
    """日期"""
    def __init__(self, init_time: datetime.datetime = None):
        if init_time is None:
            self._date = datetime.datetime.today()
        else:
            self._date = init_time

    def add_days(self, day):
        self._date += datetime.timedelta(day)

    def add_month(self, month: int):
        new = self.month + month
        if new == 0:
            ryear = -1
            rmon = 12
        else:
            ryear = new // 12
            rmon = new % 12
        day = self._date.day
        new_date = datetime.datetime(self.year + ryear, rmon, 1, self.hour, self.minute, self.second)
        new_date += datetime.timedelta(day - 1)
        while new_date.month != rmon:
            new_date -= datetime.timedelta(1)
        self._date = new_date

    def add_year(self, year: int):
        new_date = datetime.datetime(self.year + year, self.month, 1, self.hour, self.minute, self.second)
        new_date += datetime.timedelta(self.day - 1)
        self._date = new_date

    def add_hour(self, hour: int):
        self._date += datetime.timedelta(hours=hour)

    def add_minute(self, minute: int):
        self._date += datetime.timedelta(minutes=minute)

    def add_second(self, second: int):
        self._date += datetime.timedelta(seconds=second)

    def set_date(self, year: int, month: int, day: int):
        self._date = datetime.datetime(year, month, day)

    def set_time(self, time: datetime.datetime):
        self._date = time

    @property
    def year(self):
        return self._date.year

    @property
    def month(self):
        return self._date.month

    @property
    def day(self):
        return self._date.day

    @property
    def date(self):
        return self.year, self.month, self.day

    @property
    def hour(self):
        return self._date.hour

    @property
    def minute(self):
        return self._date.minute

    @property
    def second(self):
        return self._date.second

    @property
    def weekday(self):
        return self._date.weekday()

    def get_inter(self) -> datetime.datetime:
        return self._date

    def __str__(self):
        return self._date.isoformat()


class KLine:
    """k线"""
    def __init__(self, date: datetime.datetime, src: dict[str, int | float]):
        self.date = date  # 日期
        self.open = src['open']  # 开盘价
        self.high = src['high']  # 最高价
        self.low = src['low']  # 最低价
        self.close = src['close']  # 收盘价
        self.volume = src['volume']  # 成交量
        self.previous: KLine | None = None  # 上一日k
        self.next: KLine | None = None  # 下一日k
        self.vec: Vector | None = None  # 向量值

    @staticmethod
    def increasement(before: int | float, after: int | float):
        """计算涨幅"""
        if before == 0:
            return 0
        res = after / before - 1
        if before < 0:
            return -res
        return res

    @property
    def increase_day(self):
        """日内涨幅"""
        return self.increasement(self.open, self.close)

    @property
    def last_close(self):
        """昨日收盘价"""
        return self.previous.close if self.previous else self.open

    @property
    def increase(self):
        """涨幅"""
        return self.increasement(self.last_close, self.close)

    @property
    def high_offset(self):
        """高点偏移"""
        return self.increasement(self.open, self.high)

    @property
    def low_offset(self):
        """低点偏移"""
        return self.increasement(self.open, self.low)

    @property
    def daily_limit(self):
        """一字涨停"""
        return self.increase >= .04 and self.close == self.high == self.open

    @property
    def limit_down(self):
        """一字跌停"""
        return self.increase <= -.04 and self.close == self.low == self.open

    def ma(self, cycle: int, prop: str):
        """移动均线"""
        total = 0
        ptr = self
        i = 0
        while i < cycle:
            if ptr is None:
                break
            total += ptr.__getattribute__(prop)
            ptr = ptr.previous
            i += 1
        return total / i

    def ndup(self, n: int):
        """连续n日上涨"""
        ptr = self
        while n > 0:
            if ptr is None:
                return False
            if ptr.increase <= 0:
                return False
            ptr = ptr.previous
            n -= 1
        return True

    def nddown(self, n: int):
        """连续n日下跌"""
        ptr = self
        while n > 0:
            if ptr is None:
                return False
            if ptr.increase > 0:
                return False
            ptr = ptr.previous
            n -= 1
        return True

    def get_history_value(self, span: int, prop: str):
        """获取历史属性值"""
        ptr = self
        while span:
            if ptr.previous is None:
                break
            ptr = ptr.previous
            span -= 1
        return ptr.__getattribute__(prop)

    def interval_max(self, span: int, prop: str):
        """获取属性的区间最大值"""
        ptr = self
        res = ptr.__getattribute__(prop)
        while span:
            if ptr.previous is None:
                break
            ptr = ptr.previous
            if ptr.__getattribute__(prop) > res:
                res = ptr.__getattribute__(prop)
            span -= 1
        return res

    def interval_min(self, span: int, prop: str):
        """获取属性的区间最小值"""
        ptr = self
        res = ptr.__getattribute__(prop)
        while span:
            if ptr.previous is None:
                break
            ptr = ptr.previous
            if ptr.__getattribute__(prop) < res:
                res = ptr.__getattribute__(prop)
            span -= 1
        return res

    def rsi(self, m1: int = 6, m2: int = 12, m3: int = 24):
        """返回股票的rsi指标值"""
        if not m1 < m2 < m3:
            raise ValueError('参数必须从小到大排列！')
        res = []
        for c in (m1, m2, m3):
            ptr = self
            a = 0
            b = 0
            n = 0
            while ptr.previous is not None and n < c:
                ptr = ptr.previous
                n += 1
            while n:
                i = ptr.close - ptr.previous.close if ptr.previous else ptr.close - ptr.open
                if i >= 0:
                    a = ((c - 1) * a + i) / c
                else:
                    b = ((c - 1) * b + i * -1) / c
                n -= 1
                ptr = ptr.next
            res.append(0 if a == 0 else a / (a + b))
        return res

    def get_datetime(self):
        return pd.to_datetime(self.date)

    def insert(self, kline: KLine):
        """向后插入k线"""
        kline.next = self.next
        self.next = kline
        kline.previous = self
        if kline.next is not None:
            kline.next.previous = kline

    def insert_ahead(self, kline: KLine):
        """向前插入k线"""
        kline.previous = self.previous
        self.previous = kline
        kline.next = self
        if kline.previous is not None:
            kline.previous.next = kline

    def __str__(self):
        res = (
            "Open: \t{}\n".format(self.open),
            "High: \t{}\n".format(self.high),
            "Low: \t{}\n".format(self.low),
            "Close: \t{}\n".format(self.close),
            "Volume: \t{}\n".format(self.volume),
            "Increase: \t{:.4f}\n".format(self.increase),
            "Increase Day: \t{:.4f}\n".format(self.increase_day),
            "High Offset: \t{:.4f}\n".format(self.high_offset),
            "Low Offset: \t{:.4f}\n".format(self.low_offset),
            "mva5: \t{:.1f}\n".format(self.ma(5, 'volume')),
            "mva10: \t{:.1f}\n".format(self.ma(10, 'volume')),
            "ma5: \t{:.4f}\n".format(self.ma(5, 'close')),
            "ma10: \t{:.4f}\n".format(self.ma(10, 'close')),
            "3dup: \t{}\n".format(self.ndup(3)),
            "3ddown: \t{}".format(self.nddown(3))
        )
        return "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(*res)

    @property
    def evaluate(self):
        """评估文本"""
        res = ''
        ma5 = self.ma(5, 'close')
        ma10 = self.ma(10, 'close')
        his = self.interval_max(10, 'close')
        res += str(self)
        res += '\nma5>ma10? \t{}'.format(ma5 > ma10)
        res += '\nclose/ma10 \t{:.4f}'.format(self.increasement(ma10, self.close))
        res += '\nhigh/ma10 \t{:.4f}'.format(self.increasement(ma10, self.high))
        res += '\nclose/ma5 \t{:.4f}'.format(self.increasement(ma5, self.close))
        res += '\nclose/max10 \t{:.4f}'.format(self.increasement(his, self.close))
        return res

    @property
    def candle(self):
        """返回绘制蜡烛图使用的数据"""
        date = []
        res = []
        ptr = self
        while ptr is not None:
            date.insert(0, ptr.date)
            res.insert(0, (ptr.open, ptr.high, ptr.low, ptr.close, ptr.volume,
                           ptr.close - ptr.last_close, ptr.increase * 100, ptr.last_close,
                           ptr.ma(5, 'close'), ptr.ma(10, 'close'), ptr.ma(20, 'close')))
            ptr = ptr.previous
        ptr = self.next
        while ptr is not None:
            date.append(ptr.date)
            res.append((ptr.open, ptr.high, ptr.low, ptr.close, ptr.volume,
                        ptr.close - ptr.last_close, ptr.increase * 100, ptr.last_close,
                        ptr.ma(5, 'close'), ptr.ma(10, 'close'), ptr.ma(20, 'close')))
            ptr = ptr.next
        columns = ['open', 'high', 'low', 'close', 'volume',
                   'change', 'pct_change', 'last_close', 'ma5', 'ma10', 'ma20']
        return pd.DataFrame(res, index=pd.DatetimeIndex(date), columns=columns)


class MarketSlice:
    """市场切片"""
    def __init__(self, stime: datetime.datetime, ctime: datetime.datetime = None, **kw):
        self._data: dict[datetime.datetime, np.ndarray[Vector]] = kw.get('data', {})  # 日k特征
        self.date_handler: Date = Date(stime)  # 日期管理器
        self._dates: list[datetime.datetime] = kw.get('dates', [])  # 日期列表
        self._date_index = 0  # 当前日期索引
        self.stime: datetime.datetime = stime  # 起始日期
        if ctime is None:
            ctime = datetime.datetime.today()
        self.ctime: datetime.datetime = ctime  # 当前（终止）日期
        self._hashtable: dict[str, int] = kw.get('hashtable', {})  # 标的哈希表
        self._quotes: dict[datetime.datetime, dict[str, Vector]] = {}  # 记录特征

    def next(self):
        """跳转至下一交易日"""
        idx = self._date_index + 1
        if idx > len(self._dates) - 1 or self._dates[idx] > self.ctime:
            return 1
        self.date_handler.set_time(self._dates[idx])
        self._date_index = idx
        return 0

    @property
    def tell(self) -> dict[str, Vector]:
        """返回当日各股特征"""
        date = self.date_handler.get_inter()
        if date in self._quotes:
            return self._quotes[date]
        if self._data and date in self._data:
            res = {}
            for k, v in self._hashtable.items():
                vec = self._data[date][v]
                if vec is not None:
                    res[k] = vec
            self._quotes[date] = res
            return res
        return {}

    @property
    def today(self) -> datetime.datetime:
        return self.date_handler.get_inter()


def _to_vec(arr: np.ndarray):
    res = np.full(arr.size, None)
    for i in range(arr.size):
        if isinstance(arr[i], KLine):
            res[i] = arr[i].vec
    return res


def get_max_cpu_count():
    count = os.cpu_count() or 1
    if sys.platform == 'win32':
        count = min(61, count)
    return count


class Market:
    """市场"""
    def __init__(self, stime: datetime.datetime, ctime: datetime.datetime = None):
        self._data: dict[datetime.datetime, np.ndarray[KLine]] = {}  # 日k数据
        self.date_handler: Date = Date(stime)  # 日期管理器
        self._dates: list[datetime.datetime] = []  # 日期列表
        self._date_index = 0  # 当前日期索引
        self.stime: datetime.datetime = stime  # 起始日期
        if ctime is None:
            ctime = datetime.datetime.today()
        self.ctime: datetime.datetime = ctime  # 当前（终止）日期
        self._hashtable: dict[str, int] = {}  # 标的哈希表
        self._quotes: dict[datetime.datetime, dict[str, KLine]] = {}  # 记录行情
        self.len: int = 200  # 标的数量
        self._slices = ()  # 多线程切片

    def load(self, src: str | dict[str, list[dict[str, str | int | float]]],
             prop: list[tuple[str, FunctionType]] = None, callback: FunctionType = None):
        if type(src) == str:
            tree = next(walk(src))[2]
            self.len = 2 * (len(tree) - 1)
            res = {}
            for i in tree:
                if i == 'date_info.pkl':
                    continue
                fp = open(src + i)
                data = json.load(fp)
                fp.close()
                index = i[:-5]
                res[index] = data
                if callback is not None:
                    ret = callback()
                    if ret != 0:
                        raise SystemError('load aborted.')
            self._load_from_obj(res, prop, callback)
        elif type(src) == dict:
            self.len = len(src)
            self._load_from_obj(src, prop, callback)
        else:
            raise TypeError('数据格式错误！')

    def _load_from_obj(self, obj: dict[str, list[dict[str, str | int | float]]],
                       prop: list[tuple[str, FunctionType]], callback: FunctionType):
        """从爬虫返回的对象加载股票数据"""
        # 先清空哈希表
        self._data.clear()
        # 加载数据
        hash_value = 0
        for index, data in obj.items():
            if index == 'date_info':
                continue
            self._hashtable[index] = hash_value
            # 数据处理
            last = None
            for data_day in data:
                # 删除date属性前记录
                date = data_day.pop('date')
                if isinstance(date, str):
                    date = date.split(' ')
                    if len(date) == 1:
                        date = date[0].split('-')
                        date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
                    else:
                        date, _time = date
                        date = date.split('-')
                        _time = _time.split(':')
                        date = datetime.datetime(
                            int(date[0]), int(date[1]), int(date[2]),
                            int(_time[0]), int(_time[1]), int(_time[2]),
                        )
                elif isinstance(date, datetime.date):
                    date = datetime.datetime(date.year, date.month, date.day)
                # 以日期作为索引存储标的日k
                if date not in self._data:
                    self._data[date] = np.full(len(obj), None)
                kline = KLine(date, data_day)
                if last is not None:
                    last.insert(kline)
                if prop is not None:
                    args = []
                    for f in prop:
                        args.append(f[1](kline))
                    kline.vec = Vector(*args)
                self._data[date][hash_value] = kline
                last = kline
            hash_value += 1
            if callback is not None:
                ret = callback()
                if ret != 0:
                    raise SystemError('load aborted.')
        self._dates = sorted(self._data.keys())
        n = ceil(get_max_cpu_count() * .5)
        self._create_slice(n)
        self._flush_index()

    @property
    def slices(self):
        """获取多线程切片"""
        return self._slices

    def _create_slice(self, count: int = None):
        """创建多线程切片"""
        if count is None:
            count = get_max_cpu_count()
        cnt = ceil(len(self._dates) / count)
        slcs = []
        for i in range(0, len(self._dates), cnt):
            sl = self._dates[i:i + cnt]
            da = {}
            for date in sl:
                da[date] = np.apply_along_axis(
                    _to_vec, 0, arr=self._data[date])
            slcs.append(MarketSlice(sl[0], sl[-1], data=da, dates=sl, hashtable=self._hashtable))
        self._slices = tuple(slcs)

    def _flush_index(self):
        """刷新当前日期索引"""
        date = self.date_handler.get_inter()
        if date in self._data:
            self._date_index = self._dates.index(date)
        else:
            self._date_index = 0
            while self._dates[self._date_index] < date:
                self._date_index += 1

    def set_time(self, _time: datetime.datetime):
        """设置时间"""
        self.date_handler.set_time(_time)
        self._flush_index()

    def get_latest_day(self):
        """获取最后一天"""
        return self._dates[-1]

    def goto_latest_day(self):
        """跳转至最后一天"""
        self.date_handler.set_time(self._dates[-1])
        self._date_index = len(self._dates) - 1

    def is_trading_day(self, _time):
        """判断是否交易日"""
        return _time in self._data

    def next(self):
        """跳转至下一交易日"""
        idx = self._date_index + 1
        if idx > len(self._dates) - 1 or self._dates[idx] > self.ctime:
            return 1
        self.date_handler.set_time(self._dates[idx])
        self._date_index = idx
        return 0

    def prior(self):
        """跳转至上一交易日"""
        idx = self._date_index - 1
        if idx < 0 or self._dates[idx] < self.stime:
            return 1
        self.date_handler.set_time(self._dates[idx])
        self._date_index = idx
        return 0

    @property
    def tell(self) -> dict[str, KLine]:
        """返回当日行情"""
        date = self.date_handler.get_inter()
        if date in self._quotes:
            return self._quotes[date]
        if self._data and date in self._data:
            res = {}
            for k, v in self._hashtable.items():
                kline = self._data[date][v]
                if kline is not None:
                    res[k] = kline
            self._quotes[date] = res
            return res
        return {}

    def get_quotes(self, now_time: datetime.datetime) -> dict[str, KLine]:
        """返回某日行情"""
        ctime = self.date_handler.get_inter()
        self.date_handler.set_time(now_time)
        res = self.tell
        self.date_handler.set_time(ctime)
        return res

    def remake(self):
        """重开（回到开始日期）"""
        if self.date_handler.get_inter() != self.stime:
            self.date_handler.set_time(self.stime)
        self._flush_index()

    def __len__(self):
        return len(self._dates)

    @property
    def today(self) -> datetime.datetime:
        return self.date_handler.get_inter()


class Order:
    """订单"""
    def __init__(self, cost: int | float, volume: int, create_time: datetime.datetime):
        self.create_time = create_time  # 建仓时间
        self.amount = cost * volume  # 持有资金
        self.volume = volume  # 持仓量
        self.current = cost  # 现价
        self.max_income_pct = 0  # 最大收益率
        self.retracement = 0  # 最大回撤幅度

    @property
    def income(self):
        return self.current * self.volume - self.amount

    @property
    def income_pct(self):
        res = self.income / self.amount if self.amount else 0
        if self.max_income_pct == 0:
            self.max_income_pct = res
        else:
            if res > self.max_income_pct:
                self.max_income_pct = res
        if self.retracement == 0 and res < 0:
            self.retracement = res
        elif res < 0 and res < self.retracement:
            self.retracement = res
        return res

    @property
    def cost(self):
        return self.amount / self.volume

    def overweight(self, volume: int):
        self.amount += volume * self.current
        self.volume += volume

    def underweight(self, volume: int):
        if volume > self.volume:
            volume = self.volume
        self.amount -= volume * self.current
        self.volume -= volume

    def __str__(self):
        res = (
                ("[多]" if self.volume >= 0 else "[空]") +
                "建仓时间：" + str(self.create_time) +
                "\n数量：" + str(self.volume) +
                "\n成本：" + str(self.cost) +
                "\n价格：" + str(self.current) +
                "\n持仓盈亏：" + "{:.2f}".format(self.income) +
                "\n盈亏百分比：" + "{:.2f}".format(self.income_pct * 100)
        )
        return res


class Investor:
    """投资者"""
    def __init__(self, market: Market):
        self.market = market  # 投资的市场
        self.li_buy: set[str] = set()  # 买入集合
        self.li_sell: set[str] = set()  # 卖出集合
        self.li_t: set[str] = set()  # 做T集合
        self._warehouse: dict[str, Order] = {}  # 持仓信息
        self.strategy_history: dict[datetime.datetime, tuple[set[str], set[str], set[str]]] = {}  # 历史策略
        self.warehouse_history: dict[datetime.datetime, list[tuple[str, datetime.datetime, int | float]]] = {}  # 历史持仓
        self._win: int = 0  # 盈利次数（统计胜率用）
        self._lose: int = 0  # 亏损次数（统计胜率用）
        self._li_unsale: set[str] = set()  # 因为跌停而没有卖出的股票
        self._income_rate = 0  # 累计收益率
        self._value = 1  # 单位净值
        self._static = {}  # 静态变量
        # 历史记录
        self.history_date: list[datetime.datetime] = []  # 历史记录日期列
        self.history_floating: list[int | float] = []  # 历史记录浮盈列
        self.history_income_rate: list[int | float] = []  # 历史记录累计收益率列
        self.history_value: list[int | float] = []  # 历史记录单位净值列
        self.history_operate: list[tuple[str, datetime.datetime, int, float, float, float]] = []  # 历史操作记录

    @property
    def static(self):
        """静态变量的获取方法"""
        return self._static

    def get_value(self):
        """返回单位净值"""
        level = 100000000
        pr = 2
        mod = self._value // (level / pow(10, pr))
        if mod > pow(10, pr):
            return f'{mod / pow(10, pr):.2f}亿'
        return f'{self._value: .4f}'

    def get_income_rate(self):
        """返回累计收益率"""
        return self._income_rate

    def get_signal(self, symbol: str):
        """返回操作信号"""
        res = []
        date = []
        for k, v in self.strategy_history.items():
            sig = [None, None, None]
            info = self.market.get_quotes(k)
            flag = False
            for i in range(3):
                if symbol in v[i]:
                    kline = info[symbol]
                    if kline.next:
                        sig[i] = kline.next.low * .99 if not i % 2 else kline.next.high * 1.01
                    else:
                        flag = True
                        break
            if flag:
                break
            if sig.count(None) != 3:
                date.append(info[symbol].next.date)
                res.append(sig)
        columns = ['buy', 'sell', 't']
        return pd.DataFrame(res, index=pd.DatetimeIndex(date), columns=columns)

    def update(self) -> bool:
        """刷新方法"""
        # 买入卖出求交集得出做t列表
        self._update_t()
        # 记录今日策略和持仓
        self._record_history()
        # 前进到下一交易日
        if self.market.next() == 1:
            return False
        # 处理未卖出
        for symbol in self._li_unsale.copy():
            self.sell(symbol)
        # 模拟买入操作
        while self.li_buy:
            self.buy(self.li_buy.pop())
        # 模拟卖出操作
        for k in self.li_sell:
            self.sell(k)
        # 模拟做t操作
        while self.li_t:
            self.t(self.li_t.pop())
        # 更新持仓价格
        for k, v in self._warehouse.items():
            if k in self.market.tell:
                v.current = self.market.tell[k].close
        # 计算今日收益率
        n = len(self._warehouse)
        rate = 0
        for k in self.li_sell:
            ac = self._sell_account(k)
            rate += ac
            self._income_rate += ac
        if n:
            rate /= n
        # 更新单位净值
        self._value *= (1 + rate)
        # 记录今日浮盈、累计收益率和单位净值
        self.li_sell.clear()
        self.history_date.append(self.market.date_handler.get_inter())
        self.history_floating.append(self.floating)
        self.history_income_rate.append(self._income_rate)
        self.history_value.append(self._value)
        return True

    def _update_t(self):
        self.li_t.update(self.li_buy.intersection(self.li_sell))
        self.li_buy.difference_update(self.li_t)
        self.li_sell.difference_update(self.li_t)

    def _record_history(self, warehouse=True):
        date = self.market.date_handler.get_inter()
        self.strategy_history[date] = (self.li_buy.copy(), self.li_sell.copy(), self.li_t.copy())
        if not warehouse:
            return
        self.warehouse_history[date] = [(k, v.create_time, v.income_pct) for k, v in self._warehouse.items()]

    def _sell_account(self, symbol: str):
        """计算卖出收益"""
        if symbol in self._warehouse:
            res = self._warehouse[symbol].income_pct
            del self._warehouse[symbol]
            return res
        return 0

    def buy(self, symbol: str):
        """模拟买入"""
        if symbol not in self.market.tell:
            return
        self._buy(symbol)

    def _buy(self, symbol: str):
        volume = 100
        if symbol not in self._warehouse:
            self._warehouse[symbol] = Order(self.market.tell[symbol].low, volume, self.market.date_handler.get_inter())
        else:
            self._warehouse[symbol].current = self.market.tell[symbol].low
            self._warehouse[symbol].overweight(volume)

    def sell(self, symbol: str):
        """模拟卖出"""
        if symbol not in self._warehouse:
            return
        if symbol not in self.market.tell:
            return
        self._sell(symbol)

    def _sell(self, symbol: str):
        order = self._warehouse[symbol]
        order.current = self.market.tell[symbol].high
        if order.income_pct > 0:
            self._win += 1
        else:
            self._lose += 1
        rec = (
            symbol, order.create_time,
            (self.market.today - order.create_time).days,
            order.max_income_pct, order.retracement, order.income_pct
        )
        self.history_operate.append(rec)

    def t(self, symbol: str):
        """模拟做t"""
        if symbol not in self.market.tell:
            return
        self._t(symbol)

    def _t(self, symbol: str):
        if symbol in self._warehouse:
            volume = self._warehouse[symbol].volume
            self._warehouse[symbol].current = self.market.tell[symbol].low
            self._warehouse[symbol].overweight(volume)
        else:
            self._warehouse[symbol] = Order(self.market.tell[symbol].low, 100, self.market.date_handler.get_inter())

    def settle(self):
        """结算定档"""
        n = len(self._warehouse)
        rate = 0
        for k, v in self._warehouse.items():
            self.sell(k)
            ac = v.income_pct
            rate += ac
            self._income_rate += ac
        if n:
            rate /= n
        self._value *= (1 + rate)
        self.history_date.append(self.market.date_handler.get_inter())
        self.history_floating.append(self.floating)
        self.history_income_rate.append(self._income_rate)
        self.history_value.append(self._value)

    @property
    def floating(self):
        """浮动收益率"""
        res = 0
        for v in self._warehouse.values():
            res += v.income_pct
        n = len(self._warehouse)
        return 0 if n == 0 else res / n

    @property
    def win_rate(self):
        """胜率"""
        return self._win / (self._win + self._lose) if self._win != 0 else 0


class InvestorChina(Investor):
    """中国投资者：加入涨跌停，限制整百交易"""
    def buy(self, symbol: str):
        if symbol not in self.market.tell:
            return
        if self.market.tell[symbol].daily_limit:
            return
        self._buy(symbol)

    def sell(self, symbol: str):
        if symbol not in self._warehouse:
            return
        if symbol not in self.market.tell:
            return
        if self.market.tell[symbol].limit_down:
            self._li_unsale.add(symbol)
            return
        self._sell(symbol)
        if symbol in self._li_unsale:
            self._li_unsale.remove(symbol)

    def t(self, symbol: str):
        if symbol not in self.market.tell:
            return
        if symbol in self._warehouse and self.market.tell[symbol].limit_down:
            self._li_unsale.add(symbol)
            return
        self._t(symbol)


class InvestorTest(Investor):
    """测试投资者：只更新操作列表不模拟交易"""
    def update(self):
        self._update_t()
        self._record_history(False)
        if self.market.next() == 1:
            return False
        self.li_buy.clear()
        self.li_sell.clear()
        self.li_t.clear()
        return True
