from __future__ import annotations

import math
from math import sqrt, acos
from types import NoneType


class Vector:
    trans_func = {
        int: lambda x: x,
        float: lambda x: x,
        bool: lambda x: 1 if x else -1,
        NoneType: lambda x: 0
    }

    def __init__(self, a, *args):
        self._args = []
        self._args.append(self._to_numeric(a))
        for i in args:
            self._args.append(self._to_numeric(i))
        self._args = tuple(self._args)

    def get_args(self):
        return self._args

    @staticmethod
    def _to_numeric(_in):
        func = Vector.trans_func.get(type(_in), lambda x: 1)
        return func(_in)

    def __len__(self):
        return len(self._args)

    def __getitem__(self, item):
        return self._args[item]

    def __eq__(self, other):
        return self._args == other.get_args()

    def __hash__(self):
        return hash(self._args)

    @property
    def mod(self):
        """取模"""
        res = 0
        for i in self._args:
            res += i ** 2
        return sqrt(res)

    def dot(self, a: Vector):
        """点乘"""
        if len(a) != len(self):
            raise ValueError('两向量必须拥有相同的维度！')
        res = 0
        for i in range(len(self)):
            res += self._args[i] * a[i]
        return res

    def dot_mod(self, a: Vector):
        """返回点乘值和取模值"""
        if len(a) != len(self):
            raise ValueError('两向量必须拥有相同的维度！')
        dot = 0
        mod_self = 0
        mod_a = 0
        for i in range(len(self)):
            dot += self._args[i] * a[i]
            mod_self += self._args[i] ** 2
            mod_a += a[i] ** 2
        return dot, sqrt(mod_self), sqrt(mod_a)

    def angle(self, a: Vector):
        """求夹角"""
        return acos(round(self.dot(a) / self.mod / a.mod, 6))

    def similarity(self, a: Vector):
        """计算两个向量的相似度"""
        dot, mod_a, mod_b = self.dot_mod(a)
        if mod_a > mod_b:
            mod_a, mod_b = mod_b, mod_a
        if mod_a == 0:
            if mod_b == 0:
                return 1
            else:
                return 0
        else:
            score_mod = 2 - mod_b / mod_a
        cos = dot / mod_a / mod_b
        if cos < -1:
            cos = -1
        elif cos > 1:
            cos = 1
        score_angle = 1 - acos(cos) / math.pi
        res = (score_mod + score_angle) / 2
        return res
