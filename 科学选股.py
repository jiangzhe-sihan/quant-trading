from os import system

from tools import get_stock_list
import random


def random_time(stime: tuple[int, int], ctime: tuple[int, int]) -> tuple[int, int]:
    _m = ctime[1] - stime[1]
    _h = ctime[0] - stime[0]
    if _m < 0:
        _m += 60
        _h -= 1
    incr = random.randint(0, int(_h * 60) + _m)
    __h = incr // 60
    __m = incr % 60
    r_h = stime[0] + __h
    r_m = stime[1] + __m
    if r_m >= 60:
        r_m -= 60
        r_h += 1
    return r_h, r_m


def random_time_ex(*args):
    f = random.choice(args)
    t = random_time(*f)
    return t


if __name__ == '__main__':
    fs = 'fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2'
    li = get_stock_list(fs)['data']['diff']
    t1 = random_time_ex(((9, 30), (11, 30)), ((13, 0), (15, 0)))
    t2 = random_time_ex(((9, 30), (11, 30)), ((13, 0), (15, 0)))
    res = random.choice(li)
    print(f'明天{t1[0]:02}：{t1[1]:02}，买入\'[{res["f13"]}.{res["f12"]}]{res["f14"]}\'，')
    print(f'并在第二天{t2[0]:02}：{t2[1]:02}卖出。')
    print('稳赚不赔！')
    system('pause')
