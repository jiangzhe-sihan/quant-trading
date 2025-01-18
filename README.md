# 自研量化交易系统
探索程序交易可能性，发现上涨股票特征。

    注意：此分支是自研量化交易系统的源码部分
## 项目简介
自研量化交易系统包含策略回测和今日发牌两个功能模块。
- 策略回测
  
  定制选股规则，填补规则漏洞。

  目前支持`代码`和`向量`两种模式的策略。


- 今日发牌
  
  探索最新行情，遨游金融市场。

## 部署运行
- 配置需求
> Disk: `20GB` and above.
> 
> Memorizes: `8GB` and above.
> 
> CPU: `1GHz` and above. `Multiprocessor` is recommended.
> 
> OperatorSystem: `Windows 10` and above, `x64` version. Non-Windows has not fully tested yet.

- 环境配置
1. 确保已经安装`Python 3.10`及以上版本，执行环境正常。
2. 使用`pip`指令安装以下软件包：
```shell
pip install requests
pip install aiohttp
pip install mttkinter
pip install numpy
pip install pandas
pip install matplotlib
pip install mplfinance
```
- 启动程序

将此部分源码放在一个`src`文件夹当中，执行以下脚本即可启动自研量化交易系统：
```shell
cd .\src
python main.py
```
或是在`Windows`下运行配置部分中的`start.bat`来启动应用程序。
## 更新记录
### 2025/1/18
- 新增 在行情走势图中显示成交额和换手率
- 调整了市值的计算方法
### 2024/11/21
- 为代码模式添加多线程选项
```
注意阅读程序当中的提示，目前在代码模式中启用多线程可能会导致运行结果出现偏差。
```
- 修复若干bug
### 2024/11/16
- 为部分K线属性添加别名，简化调用
```text
ref -> get_history_value
hhv -> interval_max
llv -> interval_min
```
- 新增内置股票池：
  - 美股
  - 港股
- 修复若干bug，提高系统稳定性
### 2024/4/6
- 修复部分标的无法联网查询的问题
- 修复某些情况下添加策略描述导致策略无法加载的问题
- 新增K线属性：
  - bia(n, func) -> 计算指标乖离率
### 2024/2/16
- 支持向周期属性（移动均线，历史值，区间最值）中传入自定方法
> 下面是一个示例：
> ```python
> ma(5, lambda x: x.close) -> 计算5日收盘价均线
> ```
> 等效于
> ```python
> ma(5, 'close') -> 计算5日收盘价均线
> ```

> 使用自定义方法能够更加灵活地统计K线属性：
> ```python
> # 计算真实波幅值的方法
> def f_tr(x: KLine):
>     return max(
>         max(x.high - x.low, abs(x.previous.close - x.high if x.previous else x.close - x.high)),
>         abs(x.previous.close - x.low if x.previous else x.close - x.low)
>     )
> ```
> 向`ma`属性中传入该方法可轻松地计算ATR
> ```python
> ma(14, f_tr) -> 计算平均真实波幅（ATR）
> ```
- 新增K线属性：
  - atr(n=14) -> 计算平均真实波幅（ATR）
  - ema(n, func) -> （测试）计算移动指数平均值
### 2024/2/13
- 新增K线属性：
  - count(func, interval=0) -> 统计区间内符合条件的K线数量。默认统计全部K线。
- 增加`导出操作信号`功能
- 删除 ~~复制每一天~~ 功能
### 2024/1/31
- 修复了卖出目标价设置无效的问题
### 2024/1/23
- 新增3个内置股票池：
  - 沪深主板
  - 创业板
  - 科创板
- 全新K线属性可用：
  - 市值（market_value）
  - 换手（hs）
  - 量比（lb）
- 支持在代码策略中设置买/卖目标价：`open`, `high`, `low`, `close`
- 修复若干bug
### 2023/11/4
- 修改累计收益率统计方式
- 优化数字的格式化显示
### 2023/10/16
- 增加日志功能，保存在`log.txt`中。
- 支持单标的操作记录、盈亏汇总、最大收益与回撤查看。
- 支持将操作记录导出为CSV。
### 2023/9/1
- 为定制策略添加向量模式。