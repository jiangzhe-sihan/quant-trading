import json
import pickle
import random
import time
import winreg

from os import path, mkdir
from typing import Iterable

import requests
import aiohttp
import asyncio
import logging

from general_thread import ProgressThread, MultiThreadLoader


def init():
    logging.basicConfig(
        filename='log.txt',
        format='%(asctime)s [%(levelname)s] %(message)s',
        level=logging.INFO,
        encoding='utf-8'
    )
    if not path.exists('../channels'):
        mkdir('../channels')
    if not path.exists('../data'):
        mkdir('../data')
    if not path.exists('../pools'):
        mkdir('../pools')
    if not path.exists('../strategies'):
        mkdir('../strategies')
    if not path.exists('../configure.json'):
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
    if not path.exists('../configure.json'):
        return {}
    fp = open('../configure.json')
    res = json.load(fp)
    fp.close()
    return res


def save_config(cfg: dict):
    ori = load_config()
    if cfg != ori:
        fp = open('../configure.json', 'w+')
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
    flag = [False]

    async def get():
        while True:
            try:
                if flag[0]:
                    return
                async with session.get(url, **kw) as resp:
                    try:
                        r = await resp.text()
                        await asyncio.sleep(.1)
                        if resp.status == 403:
                            await asyncio.sleep(.5)
                            continue
                        flag[0] = True
                        return r
                    except TimeoutError:
                        resp.close()
                        raise TimeoutError('连接超时')
                    except Exception as e:
                        resp.close()
                        raise e
            except aiohttp.ServerDisconnectedError:
                await asyncio.sleep(.5)
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


def get_aio_session() -> aiohttp.ClientSession:
    return aiohttp.ClientSession()


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


def get_stock_list(fs):
    ua = get_user_agent()
    url = 'http://{}.push2.eastmoney.com/api/qt/clist/get?pn=1&pz={}&po=1&np=1&fltt=2&invt=2&fid=f3&{}&fields=f12,f13,f14'
    session = requests.Session()
    res = session.get(url.format(random.randint(1, 99), 20, fs), headers={'User-Agent': ua, 'host': '73.push2.eastmoney.com'})
    count = res.json()['data']['total']
    res = session.get(url.format(random.randint(1, 99), count, fs), headers={'User-Agent': ua, 'host': '73.push2.eastmoney.com'})
    return res.json()
