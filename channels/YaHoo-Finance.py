# NAME=雅虎财经
# DESCRIPTION=通过雅虎财经获取前复权数据


def func(pool, stime, ctime, callback):
    import yfinance as yf
    import time
    # from tools import get_stock_info

    pstime = '{}-{:0>2}-{:0>2}'.format(stime[0], stime[1], stime[2])
    pctime = '{}-{:0>2}-{:0>2}'.format(ctime[0], ctime[1], ctime[2])

    poolb = pool.copy()
    for i in range(len(poolb)):
        mkt, code = poolb[i].split('.')
        if mkt == '116':
            poolb[i] = f'{code[1:]}.HK' if code.startswith('0') else f'{code}.HK'
        else:
            poolb[i] = code

    task_res = []
    gc = 66
    # gc = len(poolb)
    for i in range(0, len(poolb), gc):
        end = i + gc
        if end > len(poolb):
            end = len(poolb)
        tasks = [poolb[i] for i in range(i, end)]
        src = yf.download(tasks, start=pstime, end=pctime, group_by='ticker')
        shares = []
        res = []
        for code in src.columns.levels[0]:
            shares.append(code)
            # res.append(round(src[code], 3))
            res.append((round(src[code], 3), code))
            if callback is not None:
                ret = callback()
                if ret != 0:
                    raise SystemError('download aborted.')
        time.sleep(1)
        # nc = 20
        # info = []
        # for j in range(0, len(shares), nc):
        #     tks = shares[j:j+nc]
        #     info.extend(get_stock_info(tks))
        # for j in range(len(info)):
        #     res[j] = res[j], info[j]
        task_res.extend(res)
    
    res = {}
    for i, ss in task_res:
        li = []
        # code = ss[2]
        # sp = code.split('.')
        # exchg = sp[1] if len(sp) > 1 else 'US'
        # name = ss[1]
        # filename = '[{}.{}]{}'.format(exchg, code, name)
        
        sp = ss.split('.')
        exchg = sp[1] if len(sp) > 1 else 'US'
        code = sp[0]
        filename = '[{}.{}]{}'.format(exchg, code, code)
        for idx in range(len(i)):
            di = {}
            row_data = i.iloc[idx]
            di['date'] = row_data.name
            di['open'] = row_data['Open']
            di['close'] = row_data['Close']
            di['high'] = row_data['High']
            di['low'] = row_data['Low']
            di['volume'] = row_data['Volume']
            di['amount'] = row_data['Volume'] * row_data['Close']
            # di['shares'] = ss[0]
            # di['hs'] = 100 * row_data['Volume'] / ss[0]
            li.append(di)
        res[filename] = li
    res['date_info'] = (stime, ctime)
    return res
