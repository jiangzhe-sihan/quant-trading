import datetime
import os
import json
from types import FunctionType
from typing import Iterable

from framework import Investor, KLine, MarketSlice
from vector import Vector


def vec_filter(args: tuple[MarketSlice, list[tuple[Vector, float]], list[tuple[Vector, float]]]):
    mks, group_buy, group_sell = args
    res = {}
    while True:
        for k, v in mks.tell.items():
            for vd in group_buy:
                if v.similarity(vd[0]) > vd[1]:
                    if mks.today not in res:
                        res[mks.today] = []
                    res[mks.today].append((k, 'b'))
                    break
            for vd in group_sell:
                if v.similarity(vd[0]) > vd[1]:
                    if mks.today not in res:
                        res[mks.today] = []
                    res[mks.today].append((k, 's'))
                    break
        if mks.next() == 1:
            break
    return res


class Script:
    def __init__(self, name: str, descript: str, func: FunctionType, prop: Iterable = None, simi: float = .98):
        self.name = name
        self.description = descript
        self.func = func
        self.prop = prop
        """下面是向量脚本的属性"""
        self.simi = simi
        self.group_buy = None
        self.group_sell = None

    @classmethod
    def _load_desc(cls, fp):
        name = None
        descript = None
        simi = .98
        for line in fp:
            if not line.startswith('# '):
                break
            if line[2:].startswith('NAME='):
                name = line[7:-1]
            elif line[2:].startswith('DESCRIPTION='):
                descript = line[14:-1].replace('\\n', '\n')
            elif line[2:].startswith('SIMILARITY='):
                simi = float(line[13:-1])
        return name, descript, simi

    @classmethod
    def load_script(cls, path: str):
        fp = open(path, encoding='utf-8')
        name, descript = cls._load_desc(fp)[:2]
        func = {}
        fp.seek(0)
        exec(fp.read(), None, func)
        res = cls(name, descript, func.get('func', None), func.get('prop', None))
        fp.close()
        return res

    @classmethod
    def load_vec_script(cls, path: str):
        fp = open(path, encoding='utf-8')
        name, descript, simi = cls._load_desc(fp)
        prop = json.load(fp)
        fp.close()
        for i in range(len(prop)):
            di = {}
            exec(prop[i], None, di)
            prop[i] = (f'prop{i+1}', di['func'])
        return name, descript, prop, simi

    @classmethod
    def load_ved_script(cls, path: str):
        fp = open(path, encoding='utf-8')
        group = json.load(fp)
        group_buy_ori: list[list[float]] = group['buy']
        group_sell_ori: list[list[float]] = group['sell']
        fp.close()
        group_buy: list[tuple[Vector, float]] = []
        group_sell: list[tuple[Vector, float]] = []
        for i in group_buy_ori:
            group_buy.append((Vector(*i[:-1]), i[-1]))
        for i in group_sell_ori:
            group_sell.append((Vector(*i[:-1]), i[-1]))

        def func(self: Investor, operation: dict[datetime.datetime, list[tuple[str, str]]]):
            today = self.market.today
            if today not in operation:
                return
            for r in operation[today]:
                if r[1] == 'b':
                    self.li_buy.add(r[0])
                else:
                    self.li_sell.add(r[0])

        return func, group_buy, group_sell


class ScriptLoader:
    def __init__(self, pwd: str, ltype: str, ex_name: str = '.py'):
        self._ex_name = ex_name
        self._li_scripts = set()
        self._pwd = pwd
        self._ltype = ltype
        self._script_instance: dict[str, tuple[Script, float]] = {}
        self._inited = True
        self._update()

    def get_init(self):
        return getattr(self, '_inited', False)

    def get_script_list(self):
        self._update()
        return sorted(self._li_scripts)

    def _update(self):
        tree = next(os.walk(self._pwd))
        cur = set()
        for i in tree[2]:
            if i.endswith(self._ex_name):
                cur.add(i[:-len(self._ex_name)])
        if self._li_scripts != cur:
            self._li_scripts = cur

    def get_script(self, filename: str) -> Script:
        self._update()
        if filename not in self._li_scripts:
            raise KeyError('%s%s不存在' % (self._ltype, filename))
        path = self._pwd + filename + self._ex_name
        mtime = os.path.getmtime(path)
        if filename not in self._script_instance:
            sp = Script.load_script(path)
            self._script_instance[filename] = (sp, mtime)
        elif mtime > self._script_instance[filename][1]:
            sp = Script.load_script(path)
            self._script_instance[filename] = (sp, mtime)
        return self._script_instance[filename][0]


class StrategyLoader(ScriptLoader):
    instance = {}

    def __new__(cls, *args, **kwargs):
        if args:
            pwd = args[0]
        elif 'pwd' in kwargs:
            pwd = kwargs['pwd']
        else:
            pwd = '../strategies/'
        if pwd not in cls.instance:
            cls.instance[pwd] = super().__new__(cls)
        return cls.instance[pwd]

    def __init__(self, pwd: str = '../strategies/'):
        if not self.get_init():
            super().__init__(pwd, '策略')

    def get_strategy_list(self):
        return self.get_script_list()

    def get_strategy(self, filename: str):
        return self.get_script(filename)


class ChannelLoader(ScriptLoader):
    instance = {}

    def __new__(cls, *args, **kwargs):
        if args:
            pwd = args[0]
        elif 'pwd' in kwargs:
            pwd = kwargs['pwd']
        else:
            pwd = '../channels/'
        if pwd not in cls.instance:
            cls.instance[pwd] = super().__new__(cls)
        return cls.instance[pwd]

    def __init__(self, pwd: str = '../channels/'):
        if not self.get_init():
            super().__init__(pwd, '频道')

    def get_channel_list(self):
        return self.get_script_list()

    def get_channel(self, filename: str):
        return self.get_script(filename)


class JsonLoader:
    def __init__(self, pwd: str, ltype: str, ex_name: str = '.json'):
        self._ex_name = ex_name
        self._li_pools = set()
        self._pwd = pwd
        self._ltype = ltype
        self._json_instance = {}
        self._inited = True
        self._update()

    def get_init(self):
        return getattr(self, '_inited', False)

    def get_json_list(self):
        self._update()
        return sorted(self._li_pools)

    def _update(self):
        tree = next(os.walk(self._pwd))
        cur = set()
        for i in tree[2]:
            if i.endswith(self._ex_name):
                cur.add(i[:-len(self._ex_name)])
        if self._li_pools != cur:
            self._li_pools = cur

    def get_json(self, filename: str):
        self._update()
        if filename not in self._li_pools:
            raise KeyError('%s%s不存在' % (self._pwd, filename))
        path = self._pwd + filename + self._ex_name
        mtime = os.path.getmtime(path)
        if filename not in self._json_instance:
            fp = open(path, encoding='utf-8')
            res = json.load(fp)
            fp.close()
            self._json_instance[filename] = (res, mtime)
        elif mtime > self._json_instance[filename][1]:
            fp = open(path, encoding='utf-8')
            res = json.load(fp)
            fp.close()
            self._json_instance[filename] = (res, mtime)
        return self._json_instance[filename][0]


class StockPoolLoader(JsonLoader):
    instance = {}

    def __new__(cls, *args, **kwargs):
        if args:
            pwd = args[0]
        elif 'pwd' in kwargs:
            pwd = kwargs['pwd']
        else:
            pwd = '../pools/'
        if pwd not in cls.instance:
            cls.instance[pwd] = super().__new__(cls)
        return cls.instance[pwd]

    def __init__(self, pwd: str = '../pools/'):
        if not self.get_init():
            super().__init__(pwd, '股票池')

    def get_pools_list(self):
        return self.get_json_list()

    def get_pool(self, filename: str):
        return self.get_json(filename)


class VedLoader(JsonLoader):
    instance = {}

    def __new__(cls, *args, **kwargs):
        if args:
            pwd = args[0]
        elif 'pwd' in kwargs:
            pwd = kwargs['pwd']
        else:
            pwd = '../strategies/'
        if pwd not in cls.instance:
            cls.instance[pwd] = super().__new__(cls)
        return cls.instance[pwd]

    def __init__(self, pwd: str = '../strategies/'):
        if not self.get_init():
            super().__init__(pwd, 'ved脚本', '.ved')

    def get_details(self, filename):
        self._update()
        if filename not in self._li_pools:
            raise KeyError('%s%s不存在' % (self._pwd, filename))
        path = self._pwd + filename + self._ex_name
        mtime = os.path.getmtime(path)
        if filename not in self._json_instance or mtime > self._json_instance[filename][1]:
            fp = open(path, encoding='utf-8')
            res = json.load(fp)
            fp.close()
            for i in range(len(res['buy'])):
                res['buy'][i] = Vector(*res['buy'][i][:-1]), res['buy'][i][-1]
            for i in range(len(res['sell'])):
                res['sell'][i] = Vector(*res['sell'][i][:-1]), res['sell'][i][-1]
            self._json_instance[filename] = (res, mtime)
        return self._json_instance[filename][0]


class VectorStrategyLoader(ScriptLoader):
    instance = {}

    def __new__(cls, *args, **kwargs):
        if args:
            pwd = args[0]
        elif 'pwd' in kwargs:
            pwd = kwargs['pwd']
        else:
            pwd = '../strategies/'
        if pwd not in cls.instance:
            cls.instance[pwd] = super().__new__(cls)
        return cls.instance[pwd]

    def __init__(self, pwd: str = '../strategies/'):
        if not self.get_init():
            super().__init__(pwd, '策略', '.vec')

    def get_strategy_list(self):
        return self.get_script_list()

    def _get_script(self, filename):
        path = self._pwd + filename + self._ex_name
        name, desc, prop, simi = Script.load_vec_script(path)
        func, group_buy, group_sell = Script.load_ved_script(self._pwd + filename + '.ved')
        res = Script(name, desc, func, prop, simi)
        res.group_buy = group_buy
        res.group_sell = group_sell
        return res

    def get_strategy(self, filename: str):
        self._update()
        if filename not in self._li_scripts:
            raise KeyError('%s%s不存在' % (self._ltype, filename))
        path = self._pwd + filename + '.ved'
        mtime = os.path.getmtime(path)
        if filename not in self._script_instance:
            sp = self._get_script(filename)
            self._script_instance[filename] = (sp, mtime)
        elif mtime > self._script_instance[filename][1]:
            sp = self._get_script(filename)
            self._script_instance[filename] = (sp, mtime)
        return self._script_instance[filename][0]

    def append(self, filename: str, sample: KLine, loc: str):
        if loc not in ('b', 's'):
            raise ValueError(f'无法解析的添加位置"{loc}"')
        sp = self.get_strategy(filename)
        args = [f[1](sample) for f in sp.prop]
        args.append(sp.simi)
        fp = open(self._pwd + filename + '.ved', 'r+', encoding='utf-8')
        group = json.load(fp)
        if loc == 'b':
            group['buy'].append(args)
            fp.seek(0)
            json.dump(group, fp)
            fp.close()
        elif loc == 's':
            group['sell'].append(args)
            fp.seek(0)
            json.dump(group, fp)
            fp.close()

    def pop(self, filename: str, loc: str, index: int = 0):
        if loc not in ('b', 's'):
            raise ValueError(f'无法解析的弹出位置"{loc}"')
        fp = open(self._pwd + filename + '.ved', 'r+', encoding='utf-8')
        group = json.load(fp)
        fp.close()
        if loc == 'b':
            group['buy'].pop(index)
            fp = open(self._pwd + filename + '.ved', 'w+', encoding='utf-8')
            json.dump(group, fp)
            fp.close()
        elif loc == 's':
            group['sell'].pop(index)
            fp = open(self._pwd + filename + '.ved', 'w+', encoding='utf-8')
            json.dump(group, fp)
            fp.close()

    def hit_list(self, filename: str, sample: KLine):
        vl = VedLoader()
        detail = vl.get_details(filename)
        args = []
        for f in self.get_strategy(filename).prop:
            args.append(f[1](sample))
        vec = Vector(*args)
        res = {'buy': [], 'sell': []}
        for i in range(len(detail['buy'])):
            if detail['buy'][i][0].similarity(vec) > detail['buy'][i][1]:
                res['buy'].append(i)
        for i in range(len(detail['sell'])):
            if detail['sell'][i][0].similarity(vec) > detail['sell'][i][1]:
                res['sell'].append(i)
        return res

    def update(self, filename: str, simi: float):
        fp = open(self._pwd + filename + '.ved', 'r+', encoding='utf-8')
        detail = json.load(fp)
        fp.close()
        for i in detail['buy']:
            i[-1] = simi
        for i in detail['sell']:
            i[-1] = simi
        fp = open(self._pwd + filename + '.ved', 'w+', encoding='utf-8')
        json.dump(detail, fp)
        fp.close()
        fp = open(self._pwd + filename + '.vec', 'r+', encoding='utf-8')
        content = fp.readlines()
        fp.close()
        for i in range(len(content)):
            if content[i].startswith('# SIMILARITY='):
                content[i] = '# SIMILARITY=' + str(simi) + '\n'
                break
        content = ''.join(content)
        fp = open(self._pwd + filename + '.vec', 'w+', encoding='utf-8')
        fp.write(content)
        fp.close()
