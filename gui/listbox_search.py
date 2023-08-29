import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import *


class ListboxSearcher(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._fm_content = ttk.Frame(self)
        self._fm_content.pack()
        self._et_content = ttk.Entry(self._fm_content, width=16)
        self._et_content.pack(side=tk.LEFT, fill=tk.X)
        self._et_content.bind('<Key-Return>', self._on_search)
        self._et_content.bind('<Key-Next>', self._on_next)
        self._et_content.bind('<Key-Prior>', self._on_prior)
        self._bt_search = tk.Button(self._fm_content, text='🔍', relief='flat', overrelief='groove')
        self._bt_search.config(command=self._on_search)
        self._bt_search.pack(side=tk.LEFT)
        self._bt_next = tk.Button(self._fm_content, text='↓', relief='flat', overrelief='groove')
        self._bt_next.config(command=self._on_next)
        self._bt_next.pack(side=tk.LEFT)
        self._bt_prior = tk.Button(self._fm_content, text='↑', relief='flat', overrelief='groove')
        self._bt_prior.config(command=self._on_prior)
        self._bt_prior.pack(side=tk.LEFT)
        self._func_search = None
        self._func_prior = None
        self._func_next = None
        self._res_hint = tk.StringVar()
        self._lb_hint = ttk.Label(self, textvariable=self._res_hint)
        self._lb_hint.pack()
        self._li_listbox = []
        self._res = []
        self._index = -1
        self._func_hide_hint = ''

    def get_entry(self):
        return self._et_content

    def set_size(self, value):
        self._et_content.config(width=value)

    def set_search_func(self, func=None):
        self._func_search = func

    def set_prior_func(self, func=None):
        self._func_prior = func

    def set_next_func(self, func=None):
        self._func_next = func

    def _on_search(self, event=None):
        if self._func_search is None:
            self.search()
        else:
            self._func_search()

    def _on_prior(self, event=None):
        if self._func_prior is None:
            self.previous()
        else:
            self._func_prior()

    def _on_next(self, event=None):
        if self._func_next is None:
            self.next()
        else:
            self._func_next()

    def set_listbox(self, li):
        if li != self._li_listbox:
            self._li_listbox = li
        self.search()

    def search(self):
        content = self._et_content.get()
        self._res.clear()
        self._index = -1
        if content == '':
            self._res_hint.set('')
            return
        for idx in range(len(self._li_listbox)):
            lsb = self._li_listbox[idx]
            lsb.select_clear('0', 'end')
            for i in range(lsb.size()):
                if content in lsb.get(i):
                    self._res.append((idx, i))
        if len(self._res) == 0:
            self._lb_hint.config(foreground='red')
            self._res_hint.set('没有找到任何内容')
            if self._func_hide_hint != '':
                self.after_cancel(self._func_hide_hint)
            self._func_hide_hint = self.after(
                2500,
                lambda: self._res_hint.set('') if '/' not in self._res_hint.get() else None
            )
        else:
            self._lb_hint.config(foreground='black')
            self._res_hint.set(f'?/{len(self._res)}')

    def next(self):
        if len(self._res) == 0:
            self.bell()
            return False
        if self._index >= len(self._res) - 1:
            showerror('错误', '最后一项', parent=self.winfo_toplevel())
            return False
        self._index += 1
        self._res_hint.set(f'{self._index + 1}/{len(self._res)}')
        id_lsb, i = self.get()
        for lsb in self._li_listbox:
            lsb.select_clear('0', 'end')
        self._li_listbox[id_lsb].select_set(i)
        self._li_listbox[id_lsb].see(i)
        return True

    def previous(self):
        if len(self._res) == 0:
            self.bell()
            return False
        if self._index <= 0:
            showerror('错误', '第一项', parent=self.winfo_toplevel())
            return False
        self._index -= 1
        self._res_hint.set(f'{self._index + 1}/{len(self._res)}')
        id_lsb, i = self.get()
        for lsb in self._li_listbox:
            lsb.select_clear('0', 'end')
        self._li_listbox[id_lsb].select_set(i)
        self._li_listbox[id_lsb].see(i)
        return True

    def get(self):
        return self._res[self._index]
