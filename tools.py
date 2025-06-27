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

from general_thread import ProgressThread, MultiThreadLoader
import template
import numpy


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


STOCK_INFO = {}
STOCK_UNCOVERED = []


def get_stock_info(code: str):
    nlpt = template.get_pool_path() + '.cache/nl'
    if not STOCK_INFO:
        if path.exists(nlpt) and path.getsize(nlpt) and path.getmtime(nlpt) - time.time() > -86400:
            with open(nlpt, 'rb') as fp:
                STOCK_INFO.update(pickle.load(fp))
    mkt, symbol = code.split('.')
    if symbol in STOCK_INFO:
        return STOCK_INFO[symbol]
    if code in STOCK_UNCOVERED:
        gc = 50
        ua = get_user_agent()
        session = requests.Session()
        url = 'https://push2.eastmoney.com/api/qt/ulist/get?fltt=1&invt=2&fields=f14,f12,f13,f39&{}&pn=1&np=1&pz=50'
        for i in range(0, len(STOCK_UNCOVERED), gc):
            dis = {}
            fs = f'secids={",".join(STOCK_UNCOVERED[i:i+gc])}'
            resp = session.get(url.format(fs), headers={'User-Agent': ua, 'Host': 'push2.eastmoney.com'})
            for j in json.loads(resp.text)['data']['diff']:
                dis[j['f12']] = j['f14'], int(j['f39']) if j['f39'] != '-' else numpy.nan
            STOCK_INFO.update(dis)
        with open(nlpt, 'wb') as fp:
            pickle.dump(STOCK_INFO, fp)
        STOCK_UNCOVERED.clear()
        return STOCK_INFO[symbol]
    if mkt in ('0', '1'):
        fs = template.CommonPool.refer['** 沪深京全A **']
    elif mkt == '116':
        fs = template.CommonPool.refer['** 港  股 **']
    else:
        fs = 'fs=m:105,m:106,m:107'
    get_stock_list(fs)
    if symbol in STOCK_INFO:
        return STOCK_INFO[symbol]
    STOCK_UNCOVERED.append(code)
    return code, numpy.nan


async def get_stocks(session, sem, url, s, p, fs, ua):
    res = await aio_get(
        session, url.format(s, p, fs), sem,
        headers={
            'User-Agent': ua, 'Host': 'push2.eastmoney.com',
            'Referer': 'https://quote.eastmoney.com/center/gridlist.html',
        }
    )
    return res


def get_stock_list(fs):
    pt = template.get_pool_path() + '.cache/' + fs[3:].replace(':', '')
    nlpt = template.get_pool_path() + '.cache/nl'
    if path.exists(pt) and path.getsize(pt) and path.getmtime(pt) - time.time() > -86400:
        with open(pt, 'rb') as fp:
            return pickle.load(fp)
    ua = get_user_agent()
    url = 'http://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=1&np=1&fltt=2&invt=2&fid=f3&{}&fields=f14,f12,f13,f39'
    session = requests.Session()
    s = 1
    p = 100
    res = session.get(url.format(s, p, fs), headers={'User-Agent': ua, 'Host': 'push2.eastmoney.com'})
    lis = []
    dis = {}
    for i in res.json()['data']['diff']:
        lis.append(f'{i["f13"]}.{i["f12"]}')
        dis[i['f12']] = i['f14'], int(i['f39']) if i['f39'] != '-' else numpy.nan
    count = res.json()['data']['total']
    if count <= p:
        with open(pt, 'wb') as fp:
            pickle.dump(lis, fp)
        STOCK_INFO.update(dis)
        with open(nlpt, 'wb') as fp:
            pickle.dump(STOCK_INFO, fp)
        return lis
    e, r = count // p, count % p
    if r:
        e += 1
    loop = new_event_loop()
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
            dis[j['f12']] = j['f14'], int(j['f39']) if j['f39'] != '-' else numpy.nan
    with open(pt, 'wb') as fp:
        pickle.dump(lis, fp)
    STOCK_INFO.update(dis)
    with open(nlpt, 'wb') as fp:
        pickle.dump(STOCK_INFO, fp)
    return lis


def is_legal_file_name(filename: str):
    if len(re.findall(r'[\\/:*?"<>|]', filename)) > 0:
        return False
    return True
