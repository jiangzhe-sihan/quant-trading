# NAME=小鸟叼食
# DESCRIPTION=筛选出形成小鸟叼食的形态的股票。只提示买入不提示卖出。早起的鸟儿有虫吃~


def func(self):
    # 遍历所有股票（k是标的，v是k线）
    for k, v in self.market.tell.items():
        ma5 = v.ma(5, 'close')  # 计算5日收盘价均线
        ma10 = v.ma(10, 'close')  # 计算10日收盘价均线
        ma20 = v.ma(20, 'close')  # 计算20日收盘价均线
        ma30 = v.ma(30, 'close')  # 计算30日收盘价均线
        seq = [(ma5, 5), (ma10, 10), (ma20, 20), (ma30, 30)]  # 标记均线周期稍后进行排序
        seq.sort(key=lambda x: x[0])  # 升序排序
        if seq[0][1] == 5 and seq[1][1] == 10 and seq[2][1] == 20 and seq[3][1] == 30:
            # 当均线形成空头序列时
            his = v.get_history_value(2, 'close')  # 得到2天前的收盘价
            if v.open < ma5 and (v.close - his) / his < -.091:
                # 开盘价小于5日均线且当天收盘价相对于2天前的收盘价下跌了9.1%时
                self.li_buy.add(k)  # 买入
        elif seq[0][1] == 10:
            # 10日线为最低均线时
            if v.close > ma20:
                # 收盘价在20日线上方
                self.li_buy.add(k)  # 买入
