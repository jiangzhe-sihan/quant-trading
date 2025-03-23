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
pip install pypinyin
pip install numba
```
- 启动程序

在[配置目录](https://github.com/jiangzhe-sihan/quant-trading/tree/profile)下新建`src`文件夹，将此部分源码放入`src`文件夹中，执行以下脚本即可启动自研量化交易系统：
```shell
cd .\src
python main.py
```
或是在`Windows`下运行配置部分中的`start.bat`来启动应用程序。
## 更新记录
### 2025/3/23
- 修复 加载情况下关闭窗口程序无法结束的问题
- 新增 操作记录表单支持内置排序
- 新增kl属性：
  - every(func, interval) -> 判断是否每根k线都满足条件
  - exist(func, interval) -> 判断是否存在满足条件的k线
  - std(n, func) -> 计算估算标准差
- 新增 切换回测地区功能
  - 中国区：包含涨跌停交易限制
  - 国际区：无限制
  
  ~ 不同地区设置下回测结果会略有差别 ~
- 新增 更加丰富的统计数据
- 优化 页面流畅度和显示效果
### 2025/3/18
- 新增 允许在回测时访问持仓数据，用户可以基于此构建止盈止损条件
- 使用`numba`进行编译加速，提高运算速度
> *该版本需要添加`numba`依赖
### 2025/3/13
- K线图更新
  - 修复K线图乱飘的问题
  - 加入估算流通市值的显示
  - 调整字体显示比例
  - 新增 鼠标右击进入K线选择模式，滚轮切换K线，再次右击退出
  - 选择模式下双击鼠标左键查看K线属性
- 指标更新
  - 新增kl属性
    - max(a,b)、min(a,b) -> 返回较大/较小值
    - between(value,a,b) -> 判断数值是否介于a和b之间
    - cross(a,b) -> 判断数值a是否上穿数值b
- 安全性更新
  - 修复一个缓存溢出的致命bug，该bug可能会导致指标计算异常
### 2025/3/8
- 新增K线属性
  - zt_price(price, vol) -> 按照指定幅度计算涨停价
  - dt_price(price, vol) -> 按照指定幅度计算跌停价
- 支持向ref指标中传入Series序列
- 进一步提高性能
### 2025/3/6
- 新增K线属性：
  - avedev(n, func) -> 计算平均绝对偏差
  - cci(n=14) -> 计算cci指标
  - name -> 标的名
  - code -> 标的代码（交易所.品种编号）
### 2025/3/4
- 修改count方法的统计逻辑，现在可以向其中传入Series数组
- 优化内存占用
### 2025/3/3
- 扩大缓存支持范围，进一步提高运算速度
- 修复向量模式无法加载的bug
- 新增kl方法：get_series(func, *args, **kw) -> 返回一个Series数组用于进一步计算
- 支持向ma、ema、sma指标中传入Series进行计算，这将返回一个包含运算结果的Series数组
- Series数组使用日期（kl.date）进行索引
- 发牌数最大值修改至1500
### 2025/2/24
- 优化搜索功能，取消全字匹配，支持拼音首字母
> *新版搜索需要添加`pypinyin`依赖
- 修复ema、sma、rsi、lwr指标的计算偏差
- 新增指标：macd(short, long, m) -> 返回(dif, dea, macd)三个数值
- 启用部分缓存提高运算速度
- 增加提示词，强化用户引导
### 2025/2/17
- 新增内置池：复杂杠杆
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