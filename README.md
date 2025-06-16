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
### 2025/6/17
- 修复了一些错误，提高程序的稳健性。
- 停止追加更新记录，计划改为用户手册。