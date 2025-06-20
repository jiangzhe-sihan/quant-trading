# NAME=雅虎财经
# DESCRIPTION=通过雅虎财经获取前复权数据


def func(pool, stime, ctime, callback):
    import yfinance as yf
    import time
    from tools import get_stock_info

    pstime = '{}-{:0>2}-{:0>2}'.format(stime[0], stime[1], stime[2])
    pctime = '{}-{:0>2}-{:0>2}'.format(ctime[0], ctime[1], ctime[2])

    poolb = pool.copy()
    for i in range(len(poolb)):
        mkt, code = poolb[i].split('.')
        if mkt == '116':
            poolb[i] = f'{code[1:]}.HK' if code.startswith('0') else f'{code}.HK'
        elif mkt == '0':
            poolb[i] = f'{code}.SZ'
        elif mkt == '1':
            poolb[i] = f'{code}.SS'
        else:
            poolb[i] = code

    task_res = []
    gc = 500
    # gc = len(poolb)
    for i in range(0, len(poolb), gc):
        end = i + gc
        if end > len(poolb):
            end = len(poolb)
        tasks = [poolb[i] for i in range(i, end)]
        src = yf.download(tasks, start=pstime, end=pctime, group_by='ticker')
        res = []
        for code in src.columns.levels[0]:
            res.append((round(src[code], 3), code))
            if callback is not None:
                ret = callback()
                if ret != 0:
                    raise SystemError('download aborted.')
        time.sleep(1)
        task_res.extend(res)
    
    res = {}
    for i, ss in task_res:
        li = []
        sp = ss.split('.')
        exchg = sp[1] if len(sp) > 1 else 'US'
        code = f'{116 if exchg == "HK" else 1 if exchg == "SS" else 0 if exchg == "SZ" else 105}.{sp[0] if exchg == "US" else f"{sp[0]:0>5}"}'
        info = get_stock_info(code)
        filename = '[{}.{}]{}'.format(exchg, sp[0], info[0])
        
        # sp = ss.split('.')
        # exchg = sp[1] if len(sp) > 1 else 'US'
        # code = sp[0]
        # filename = '[{}.{}]{}'.format(exchg, code, code)
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
            di['shares'] = info[1]
            di['hs'] = 100 * row_data['Volume'] / info[1]
            li.append(di)
        res[filename] = li
    res['date_info'] = (stime, ctime)
    return res
