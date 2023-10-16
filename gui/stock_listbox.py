import tkinter as tk
from tkinter.messagebox import *
from tkinter.ttk import Treeview

from gui.interact_candle import *
from gui.scene import SceneSetting
from gui.subwindow import SubWindow

import logging


class StockListbox(tk.Listbox):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._info = {}
        self._player = None
        self.bind('<Double-1>', self._double_click)
        self.bind('<Button-3>', self._right_click)
        self._plt = None
        self._eval_wnd = None

    def set_info(self, info, player=None):
        self._info = info
        self._player = player

    def _double_click(self, event):
        cur = self.curselection()
        if not cur:
            return
        symbol = self.get(cur[0])
        self._show_evaluate(symbol)

    def _right_click(self, event):
        cur = self.curselection()
        if not cur:
            return
        if cur[0] != self.nearest(event.y):
            return
        symbol = self.get(cur[0])
        mu = tk.Menu(self, tearoff=0)
        mu.add_command(label='查看', command=lambda: self._show_evaluate(symbol))
        mu.add_command(label='绘制k线', command=lambda: self._draw_kline(symbol))
        if SceneSetting.get_instance().strategy_mode == 'vector':
            mu.add_separator()
            mu.add_command(label='添加买点(b)', command=lambda: self._add_bp(symbol), foreground='green')
            mu.add_command(label='添加卖点(s)', command=lambda: self._add_sp(symbol), foreground='crimson')
            di_bp = {}
            di_sp = {}
            for n in SceneSetting.get_instance().strategy:
                li = SceneSetting.get_instance().strategy_loader.hit_list(n, self._info[symbol])
                if len(li['buy']) != 0:
                    di_bp[n] = li['buy']
                if len(li['sell']) != 0:
                    di_sp[n] = li['sell']
            if di_bp or di_sp:
                mu.add_separator()
                if di_bp:
                    mu.add_command(label='删除买点(b)', command=lambda: self._del_bp(di_bp, symbol), foreground='gray')
                if di_sp:
                    mu.add_command(label='删除卖点(s)', command=lambda: self._del_sp(di_sp, symbol), foreground='darkred')
        mu.post(event.x_root, event.y_root)

    def _add_bp(self, symbol):
        kline = self._info[symbol]
        for n in SceneSetting.get_instance().strategy:
            SceneSetting.get_instance().strategy_loader.append(n, kline, 'b')
        showinfo('完成', '添加成功', parent=self.winfo_toplevel())
        logging.info(f'{kline.date} {symbol} ADD_BUY')

    def _add_sp(self, symbol):
        kline = self._info[symbol]
        for n in SceneSetting.get_instance().strategy:
            SceneSetting.get_instance().strategy_loader.append(n, kline, 's')
        showinfo('完成', '添加成功', parent=self.winfo_toplevel())
        logging.info(f'{kline.date} {symbol} ADD_SELL')

    def _del_bp(self, bps, symbol):
        kline = self._info[symbol]
        for n, lip in bps.items():
            for i in lip:
                SceneSetting.get_instance().strategy_loader.pop(n, 'b', i)
        showinfo('完成', '删除成功', parent=self.winfo_toplevel())
        logging.info(f'{kline.date} {symbol} DEL_BUY')

    def _del_sp(self, sps, symbol):
        kline = self._info[symbol]
        for n, lip in sps.items():
            for i in lip:
                SceneSetting.get_instance().strategy_loader.pop(n, 's', i)
        showinfo('完成', '删除成功', parent=self.winfo_toplevel())
        logging.info(f'{kline.date} {symbol} DEL_SELL')

    def _show_evaluate(self, symbol):
        if self._eval_wnd is not None:
            self._eval_wnd.focus()
            return
        evaluate = []
        for i in SceneSetting.get_instance().strategy:
            prop = SceneSetting.get_instance().strategy_loader.get_strategy(i).prop
            if prop is None:
                continue
            evaluate.extend(prop)
        if len(evaluate) == 0:
            showinfo(symbol, self._info[symbol].evaluate, parent=self.winfo_toplevel())
            return
        self.bell()
        self._eval_wnd = SubWindow(self.winfo_toplevel())
        self._eval_wnd.title(symbol)
        self._eval_wnd.geometry('250x400')
        self._eval_wnd.attributes('-toolwindow', 2)
        tv = Treeview(self._eval_wnd, show='headings', columns=('1', '2'))
        tv.heading('1', text='属性名', anchor='w')
        tv.heading('2', text='属性值', anchor='w')
        tv.column('1', width=120)
        tv.column('2', width=120)
        tag = True
        for i in evaluate:
            i = list(i)
            i[1] = i[1](self._info[symbol])
            tv.insert('', 'end', values=i, tags=(str(tag),))
            tag = not tag
        tv.tag_configure('True', background='#E8E8E8')
        tv.tag_configure('False', background='#DFDFDF')
        tv.place(relwidth=1.0, relheight=1.0)
        self.wait_window(self._eval_wnd)
        self._eval_wnd = None

    def _draw_kline(self, symbol):
        candle = self._info[symbol].candle
        p = self._info.popitem()
        self._info.update(dict([p]))
        date = p[1].get_datetime()
        mc = mpf.make_marketcolors(
            up='forestgreen',
            down='crimson',
            edge='i',
            wick='i',
            volume='in',
            inherit=True,
        )
        style = mpf.make_mpf_style(
            gridaxis='both',
            gridstyle='-.',
            marketcolors=mc,
            rc={'font.family': 'SimHei'}
        )
        signal = self._player.get_signal(symbol) if self._player is not None else None
        self._plt = InterCandle(candle, style, symbol, signal, date)
