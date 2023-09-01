import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror, askyesno, showinfo

from template import get_kline_test_example


class VectorStrategyEditor(tk.Frame):
    def __init__(self, master, **kw):
        if 'path' in kw:
            self._path = kw.pop('path')
        else:
            self._path = 'null'
        if 'name' in kw:
            self._stg_name = kw.pop('name')
        else:
            self._stg_name = 'null'
        if 'desc' in kw:
            self._desc = kw.pop('desc')
        else:
            self._desc = 'null'
        if 'simi' in kw:
            self._simi = kw.pop('simi')
        else:
            self._simi = 'null'
        super().__init__(master, **kw)
        self._lb_dim = tk.Label(self, text='点击+号添加一个向量维度', width=32)
        self._lb_dim.pack()
        self._fm_dim = tk.Frame(self)
        self._fm_dim.pack()
        self._bt_add = ttk.Button(self, text='+', command=self._add)
        self._bt_add.pack()
        self._bt_confirm_vector = ttk.Button(self, text='保存', command=self._save)
        self._bt_confirm_vector.pack()
        self._li_dim: list[tk.Frame] = []
        self._di_local = {}

    def _add(self):
        fm_dim_edit = tk.Frame(self._fm_dim)
        fm_dim_edit.pack(pady=5, padx=5)
        tx_exps = tk.Text(fm_dim_edit, height=3, width=32, bg='#2B2B2B', fg='#A2AAAC', insertbackground='#A2AAAC')
        tx_exps.grid(row=0, column=0)
        tx_exps.insert('0.0', 'func = ')
        bt_del = ttk.Button(fm_dim_edit, text='删除', command=lambda: self._delete(fm_dim_edit))
        bt_del.grid(row=0, column=1)
        tx_exps.focus()
        self._li_dim.append(fm_dim_edit)

    def _save(self):
        li = []
        for i in range(len(self._li_dim)):
            text = self._li_dim[i].children['!text']
            content = text.get('0.0', 'end')
            self._di_local.clear()
            try:
                exec(content, None, self._di_local)
            except Exception as e:
                showerror(type(e).__name__ + f'在第{i+1}个维度', str(e), parent=self.winfo_toplevel())
                text.focus()
                return
            if 'func' not in self._di_local:
                showerror(f'错误在第{i+1}个维度', '没有定义名为`func`的方法', parent=self.winfo_toplevel())
                text.focus()
                return
            func = self._di_local['func']
            model = get_kline_test_example()
            try:
                func(model)
            except Exception as e:
                showerror(f'测试未通过在第{i+1}个维度', f'{type(e).__name__}\n{str(e)}', parent=self.winfo_toplevel())
                text.focus()
                return
            li.append(content)
        act = askyesno('你确定？', '维度保存后无法更改！', parent=self.winfo_toplevel())
        if not act:
            return
        fp = open(self._path, 'w+', encoding='utf-8')
        fp.write('# NAME=' + self._stg_name)
        fp.write('\n')
        fp.write('# DESCRIPTION=' + self._desc)
        fp.write('\n')
        fp.write('# SIMILARITY=' + str(self._simi))
        fp.write('\n\n')
        json.dump(li, fp)
        fp.close()
        fp = open(self._path[:-4] + '.ved', 'w+')
        json.dump({'buy': [], 'sell': []}, fp)
        fp.close()
        showinfo('完成', '保存成功！', parent=self.winfo_toplevel())
        self.winfo_toplevel().destroy()

    def _delete(self, widget: tk.Frame):
        self._li_dim.remove(widget)
        widget.destroy()
