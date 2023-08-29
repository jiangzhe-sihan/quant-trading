import tkinter as tk
import tkinter.ttk as ttk


class CheckBoard(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._is_all = tk.BooleanVar(value=False)
        self._ck_all = ttk.Checkbutton(self, text='全选', variable=self._is_all, command=self._select_all)
        self._ck_all.pack()
        self._lb_split = ttk.Label(self, text='-' * 50)
        self._lb_split.pack()
        self._check_status = {}

    def append(self, label, default=False):
        if label not in self._check_status:
            boo = tk.BooleanVar(value=default)
            ck_button = ttk.Checkbutton(self, text=label, variable=boo)
            ck_button.pack()
            self._check_status[label] = (ck_button, boo)

    def _select_all(self):
        if self._is_all.get():
            for v in self._check_status.values():
                v[1].set(True)
        else:
            for v in self._check_status.values():
                v[1].set(False)

    def get(self):
        res = {}
        for k, v in self._check_status.items():
            res[k] = v[1].get()
        return res

    def get_true(self):
        res = []
        for k, v in self._check_status.items():
            if v[1].get():
                res.append(k)
        return res

    def get_false(self):
        res = []
        for k, v in self._check_status.items():
            if not v[1].get():
                res.append(k)
        return res
