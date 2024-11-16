import tkinter as tk
from tkinter.messagebox import showinfo


class Interface(tk.Frame):
    def __init__(self, *arg, **kw):
        super().__init__(*arg, **kw)
        self._fm_entry = tk.Frame(self)
        self._fm_entry.pack(pady=5)
        self._fm_chaoda = tk.Frame(self._fm_entry)
        self._fm_chaoda.pack(side=tk.LEFT)
        self._fm_da = tk.Frame(self._fm_entry)
        self._fm_da.pack(side=tk.LEFT)
        self._fm_zhong = tk.Frame(self._fm_entry)
        self._fm_zhong.pack(side=tk.LEFT)
        self._fm_xiao = tk.Frame(self._fm_entry)
        self._fm_xiao.pack(side=tk.LEFT)
        self._lb_chaoda = tk.Label(self._fm_chaoda, text='超大金额')
        self._lb_chaoda.pack()
        self._et_chaoda = tk.Entry(self._fm_chaoda, width=10)
        self._et_chaoda.pack()
        self._lb_da = tk.Label(self._fm_da, text='大单金额')
        self._lb_da.pack()
        self._et_da = tk.Entry(self._fm_da, width=10)
        self._et_da.pack()
        self._lb_zhong = tk.Label(self._fm_zhong, text='中单金额')
        self._lb_zhong.pack()
        self._et_zhong = tk.Entry(self._fm_zhong, width=10)
        self._et_zhong.pack()
        self._lb_xiao = tk.Label(self._fm_xiao, text='小单金额')
        self._lb_xiao.pack()
        self._et_xiao = tk.Entry(self._fm_xiao, width=10)
        self._et_xiao.pack()
        self._fm_button = tk.Frame(self)
        self._fm_button.pack()
        self._bt_submit = tk.Button(self._fm_button, text='计算', command=self._calc)
        self._bt_submit.pack(side=tk.LEFT, padx=5)
        self._bt_clear = tk.Button(self._fm_button, text='清空', command=self._clear)
        self._bt_clear.pack(side=tk.LEFT, padx=5)
        
    def _calc(self):
        chaoda = float(self._et_chaoda.get())
        da = float(self._et_da.get())
        zhong = float(self._et_zhong.get())
        xiao = float(self._et_xiao.get())
        li = [chaoda, da, zhong, xiao]
        li.sort()
        dis = li[-1] - li[0]
        res = (chaoda - li[0] + da - li[0]) / dis
        res1 = (li[-1] - xiao + li[-1] - zhong) / dis
        showinfo('完成', f'主力参与度为{res * 100:.2f}%\n散户参与度为{res1 * 100:.2f}', parent=self.winfo_toplevel())
    
    def _clear(self):
        self._et_chaoda.delete(0, 'end')
        self._et_da.delete(0, 'end')
        self._et_zhong.delete(0, 'end')
        self._et_xiao.delete(0, 'end')


if __name__ == '__main__':
    root = tk.Tk()
    root.title('主力参与度计算器')
    sc = Interface(root)
    sc.pack()
    root.mainloop()
