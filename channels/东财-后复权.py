# NAME=东方财富
# DESCRIPTION=使用东财的api获取后复权数据


def func(pool, stime, ctime, callback):
    from tools import get_user_agent
    from tools import new_event_loop
    from tools import get_aio_session
    from tools import aio_get
    from tools import gather
    from tools import create_semaphore
    from tools import load_config
    from configure import ChannelLoader
    import json
    import time
    from random import randint
    import re
    import asyncio
    ua = get_user_agent()

    async def get_kline(session, sem, scode):
        host = 'push2his.eastmoney.com'
        secid = ''
        s = scode.split('.')
        if s[0] == 'sh':
            secid += '1.'
        elif s[0] == 'sz':
            secid += '0.'
        else:
            secid += s[0] + '.'
        secid += s[1]
        params = {
            'cb': f'jsonp{time.time_ns() // 1000000}',
            'secid': secid,
            'ut': ''.join([f'{randint(0,65535):4x}' for _ in range(8)]),
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': '101',
            'fqt': 2,
            'end': '{}{:0>2}{:0>2}'.format(ctime[0], ctime[1], ctime[2]),
            'beg': '{}{:0>2}{:0>2}'.format(stime[0], stime[1], stime[2]),
            'rtntype': 6
        }
        r = await aio_get(
            session,
            f'http://{host}/api/qt/stock/kline/get',
            sem,
            headers={
                'User-Agent': ua,
                'Referer': 'http://quote.eastmoney.com/',
                'Host': host
            },
            params=params
        )
        await asyncio.sleep(.5)
        if callback is not None:
            ret = callback()
            if ret != 0:
                raise SystemError('download aborted.')
        return r, scode
    loop = new_event_loop()
    t = 16
    sessions = [get_aio_session() for _ in range(t)]
    sem = create_semaphore(t)
    es, er = len(pool) // t, len(pool) % t
    es += 1 if er else 0
    task = [get_kline(sessions[(i - 1) // es], sem, pool[i]) for i in range(len(pool))]
    task_res = loop.run_until_complete(gather(*task))
    for session in sessions:
        loop.run_until_complete(session.close())
    loop.close()
    res = {}
    li_unquery = []
    for i, scode in task_res:
        i = re.search(r'jsonp(.*?)\((.*)\)', i).group(2)
        try:
            i = json.loads(i)
        except json.JSONDecodeError:
            li_unquery.append(scode)
            continue
        li = []
        code = i['data']['code']
        if i['data']['market'] == 1:
            exchg = 'sh'
        elif i['data']['market'] == 0:
            exchg = 'sz'
        else:
            exchg = i['data']['market']
        name = i['data']['name']
        filename = '[{}.{}]{}'.format(exchg, code, name)
        for kline in i['data']['klines']:
            di = {}
            row_data = kline.split(',')
            di['date'] = row_data[0]
            di['open'] = float(row_data[1])
            di['close'] = float(row_data[2])
            di['high'] = float(row_data[3])
            di['low'] = float(row_data[4])
            di['volume'] = int(row_data[5]) if row_data[5] else 0
            di['amount'] = float(row_data[6]) if row_data[6] else 0
            di['hs'] = float(row_data[10]) if row_data[10] else 0
            li.append(di)
        res[filename] = li
    if li_unquery:
        chn = ChannelLoader('../channels/').get_channel(load_config()['channel'])
        res.update(chn.func(li_unquery, stime, ctime, callback))
    res['date_info'] = (stime, ctime)
    return res
