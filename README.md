# 自研量化交易系统
探索程序交易可能性，发现上涨股票特征。

    注意：此分支是自研量化交易系统的配置部分
## 更新记录
### 2023/11/5
- 添加README.md
## 目录结构解读
- channels

  存放数据源的目录。本系统中表述为数据频道。


- data

  存放数据包的目录。


- pools

  存放股票池的目录。


- strategies

  存放策略文件的目录。


- configure.json

  配置信息保存的文件。


- favicon.ico

  应用程序图标。这是运行程序所必要的。


- make.bat

  使用PyInstaller打包的脚本。


- start.bat

  应用程序启动脚本。
## 部署运行
将这些配置文件放在源码部分的上级目录中， 在`Windows`下运行配置部分中的`start.bat`来启动应用程序。