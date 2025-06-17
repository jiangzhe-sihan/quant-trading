import json
import pickle
import random
import re
import time
import winreg

from os import path, mkdir
from typing import Iterable

import requests
import aiohttp
import asyncio
import logging

from general_thread import ProgressThread, MultiThreadLoader, StockInfoPatcher
import template


def init():
    logging.basicConfig(
        filename=template.get_logging_path(),
        format='%(asctime)s [%(levelname)s] %(message)s',
        level=logging.INFO,
        encoding='utf-8'
    )
    if not path.exists(template.get_channel_path()):
        mkdir(template.get_channel_path())
    if not path.exists(template.get_data_path()):
        mkdir(template.get_data_path())
    if not path.exists(template.get_pool_path()):
        mkdir(template.get_pool_path())
    if not path.exists(template.get_pool_path() + '.cache/'):
        mkdir(template.get_pool_path() + '.cache/')
    if not path.exists(template.get_strategy_path()):
        mkdir(template.get_strategy_path())
    if not path.exists(template.get_configure_path()):
        cfg = {
            'pool': '',
            'channel': '',
            'strategy_mode': 'code',
            'strategy_code': [],
            'strategy_vector': []
        }
        save_config(cfg)


def pick(li: list, count: int):
    if count >= len(li):
        random.shuffle(li)
        res = li.copy()
        li.clear()
        return res
    res = []
    for i in range(count):
        idx = random.randint(0, len(li) - 1)
        res.append(li.pop(idx))
    return res


def load_pkl(filename: str):
    if not path.exists(filename):
        return
    fp = open(filename, 'rb')
    res = pickle.load(fp)
    fp.close()
    return res


def load_config():
    if not path.exists(template.get_configure_path()):
        return {}
    fp = open(template.get_configure_path())
    res = json.load(fp)
    fp.close()
    return res


def save_config(cfg: dict):
    ori = load_config()
    if cfg != ori:
        fp = open(template.get_configure_path(), 'w+')
        json.dump(cfg, fp)
        fp.close()


def connect(url: str = None, session: requests.Session = None, method: str = 'GET', noc: int = 1, **kw):
    def inner_connect(iurl: str, isession: requests.Session, imethod: str, callback, **ikw):
        for i in range(3):
            try:
                if isession is None:
                    match imethod.lower():
                        case 'post':
                            res = requests.post(iurl, **ikw)
                        case default:
                            res = requests.get(iurl, **ikw)
                else:
                    match imethod.lower():
                        case 'post':
                            res = isession.post(iurl, **ikw)
                        case default:
                            res = isession.get(iurl, **ikw)
                if res.status_code == 403:
                    time.sleep(.5)
                    continue
                return res
            except TimeoutError:
                raise TimeoutError('连接超时')
            except Exception as e:
                raise e
    tasks = []
    for i in range(noc):
        tasks.append(ProgressThread(inner_connect, (url, session, method), kw))
    td = MultiThreadLoader(tasks)
    td.start()
    td.join()
    res = None
    for i in td.res:
        if i.status_code == 200:
            res = i
            break
    if res is None:
        return td.res[0].text
    return res.text


async def aio_get(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore = None, **kw):
    flag = False

    async def get():
        nonlocal flag
        while True:
            try:
                if flag:
                    return
                async with session.get(url, **kw) as resp:
                    try:
                        r = await resp.text()
                        await asyncio.sleep(.1)
                        if resp.status == 403:
                            await asyncio.sleep(.5)
                            continue
                        flag = True
                        return r
                    except TimeoutError:
                        resp.close()
                        raise TimeoutError('连接超时')
                    except Exception as e:
                        resp.close()
                        raise e
            except aiohttp.ServerDisconnectedError:
                await asyncio.sleep(5)
                continue
    if sem is not None:
        async with sem:
            return await get()
    return await get()


def create_semaphore(value) -> asyncio.Semaphore:
    return asyncio.Semaphore(value)


def get_event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.get_event_loop()


def new_event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop


def get_aio_session(limit=None) -> aiohttp.ClientSession:
    connector = aiohttp.TCPConnector(limit=limit) if limit else None
    return aiohttp.ClientSession(loop=get_event_loop(), connector=connector)


def get_requests_session():
    return requests.Session()


def gather(*args):
    return asyncio.gather(*args)


def get_user_agent() -> str:
    try:
        p = r'Software\\Microsoft\\Edge\\BLBeacon'
        hkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, p)
        ev = winreg.EnumValue(hkey, 0)
        winreg.CloseKey(hkey)
        ver = ev[1]
        slc = ver.split('.')
        slc[2] = slc[3] = '0'
        ver = '.'.join(slc)
        ua = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver} Safari/537.36'
        return ua
    except:
        return 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv 11.0) like Gecko'


def print_list(li: Iterable, col: int):
    if not li:
        print('[]')
        return
    temp = 0
    print('[')
    print('\t', end='')
    for i in li:
        if temp == col:
            temp = 0
            print('\n\t', end='')
        print(i, end='\t')
        temp += 1
    print()
    print(']')


def get_stock_info(codes: list):
    tasks = [StockInfoPatcher(i) for i in codes]
    for i in tasks:
        i.start()
        time.sleep(.1)
    for i in tasks:
        i.join()
    return list(map(lambda x: x.res, tasks))


async def get_stocks(session, sem, url, s, p, fs, ua):
    n = random.randint(1, 99)
    res = await aio_get(
        session, url.format(n, s, p, fs), sem,
        headers={
            'User-Agent': ua, 'host': f'{n}.push2.eastmoney.com',
            'Referer': 'https://quote.eastmoney.com/center/gridlist.html',
        }
    )
    return res


def get_stock_list(fs):
    pt = template.get_pool_path() + '.cache/' + fs[3:].replace(':', '')
    if path.exists(pt) and path.getsize(pt) and path.getmtime(pt) - time.time() > -86400:
        with open(pt, 'rb') as fp:
            return pickle.load(fp)
    ua = get_user_agent()
    url = 'http://{}.push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=1&np=1&fltt=2&invt=2&fid=f3&{}&fields=f12,f13,f14'
    session = requests.Session()
    s = 1
    p = 50
    n = random.randint(1, 99)
    res = session.get(url.format(n, s, p, fs), headers={'User-Agent': ua, 'host': f'{n}.push2.eastmoney.com'})
    lis = []
    for i in res.json()['data']['diff']:
        lis.append(f'{i["f13"]}.{i["f12"]}')
    count = res.json()['data']['total']
    if count <= p:
        return lis
    e, r = count // p, count % p
    if r:
        e += 1
    loop = get_event_loop()
    _t = 50
    es, rs = e // _t, e % _t
    if rs:
        es += 1
    sessions = [get_aio_session() for _ in range(es)]
    sem = create_semaphore(_t)
    tasks = [get_stocks(sessions[(i - 1) // _t], sem, url, i, p, fs, ua) for i in range(2, e + 1)]
    res = loop.run_until_complete(gather(*tasks))
    for session in sessions:
        loop.run_until_complete(session.close())
    # session = get_aio_session()
    # sem = create_semaphore(_t)
    # tasks = [get_stocks(session, sem, url, i, p, fs, ua) for i in range(2, e + 1)]
    # res = loop.run_until_complete(gather(*tasks))
    # loop.run_until_complete(session.close())
    for i in res:
        for j in json.loads(i)['data']['diff']:
            lis.append(f'{j["f13"]}.{j["f12"]}')
    with open(pt, 'wb') as fp:
        pickle.dump(lis, fp)
    return lis


def is_legal_file_name(filename: str):
    if len(re.findall(r'[\\/:*?"<>|]', filename)) > 0:
        return False
    return True
