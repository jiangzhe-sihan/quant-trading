import concurrent.futures
from framework import Market
from datetime import datetime
from template import get_kline_test_example
import sys
from multiprocessing.managers import SharedMemoryManager


def filter_kl(k, v):
    if v.increase > .05:
        return k, 's'
    if v.increase < -.05:
        return k, 'b'


def main():
    for i in range(3):
        with SharedMemoryManager() as smm:
            sm = smm.SharedMemory(8)
            sm.buf[:] = MKT
        # res = []
        # with concurrent.futures.ProcessPoolExecutor() as executor:
        #     for k, v in MKT.tell.items():
        #         res.append(executor.submit(filter_kl, k, v))
        #     for fs in concurrent.futures.as_completed(res):
        #         print(fs.result())
        # for k, v in MKT.tell.items():
        #     res = filter_kl(k, v)
        #     print(res)
        if MKT.next() == 1:
            break


if __name__ == '__main__':
    MKT = Market(datetime(2022, 1, 1))
    MKT.load('../data/self_selection_A/')
    sys.setrecursionlimit(10000)
    main()
