import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import *
from gui.date_entry import DateEntry
from gui.stock_listbox import StockListbox
from gui.listbox_search import ListboxSearcher


class MarketViewer(ttk.Frame):
    def __init__(self, market, master, **kw):
        super().__init__(master, **kw)
        self._market = market
        self._player = None
        self._current_date = market.ctime
        self._searching = False
        # 界面设计
        self._fm_date_confirm = ttk.Frame(self)
        self._fm_date_confirm.pack(pady=5)
        self._lb_date = ttk.Label(self._fm_date_confirm, text='输入日期')
        self._lb_date.grid(row=0, column=0, sticky=tk.W, padx=8)
        self._de_date = DateEntry(self._fm_date_confirm)
        if market.is_trading_day(market.ctime):
            self._de_date.set(self._market.ctime)
        else:
            self._de_date.set(self._market.get_latest_day())
        self._de_date.grid(row=1, column=0, padx=5)
        self._bt_goto = ttk.Button(self._fm_date_confirm, text='转到', command=self._confirm_date, width=5)
        self._bt_goto.grid(row=1, column=1, padx=5)
        self._str_date = tk.StringVar()
        self._lb_state = ttk.Label(self, textvariable=self._str_date, font=('黑体', 12))
        self._lb_state.pack(pady=5)
        self._fm_list = ttk.Frame(self)
        self._fm_list.pack()
        self._lsb_symbol = StockListbox(self._fm_list, width=23)
        self._lsb_symbol.pack(side=tk.LEFT)
        self._scroll_symbol = ttk.Scrollbar(self._fm_list)
        self._scroll_symbol.config(command=self._lsb_symbol.yview)
        self._lsb_symbol.config(yscrollcommand=self._scroll_symbol.set)
        self._scroll_symbol.pack(side=tk.LEFT, fill=tk.Y)
        self._fm_date_button = ttk.Frame(self)
        self._fm_date_button.pack()
        self._bt_previous = ttk.Button(self._fm_date_button, text='前一天', command=self._load_previous)
        self._bt_previous.grid(row=0, column=0)
        self._bt_next = ttk.Button(self._fm_date_button, text='后一天', command=self._load_next)
        self._bt_next.grid(row=0, column=1)
        self._fm_option_button = ttk.Frame(self)
        self._fm_option_button.pack(pady=5)
        self._bt_search = ListboxSearcher(self._fm_option_button)
        self._bt_search.set_listbox([self._lsb_symbol])
        self._bt_search.pack(expand=True)
        self._confirm_date()

    def set_player(self, value):
        self._player = value
        self._confirm_date()

    def _confirm_date(self):
        date = self._de_date.get_datetime()
        if date is None:
            return
        if not self._market.is_trading_day(date):
            showerror('错误', '{}-{}-{}不是交易日！'.format(*self._de_date.get()), parent=self.winfo_toplevel())
            return
        info = self._market.get_quotes(date)
        self._current_date = date
        self._market.set_time(date)
        self._lsb_symbol.set_info(info, self._player)
        self._str_date.set('{}-{}-{}'.format(*self._de_date.get()))
        self._lsb_symbol.delete('0', 'end')
        self._lsb_symbol.insert('end', *info.keys())
        self._bt_search.search()

    def _load_previous(self):
        if self._market.prior() == 1:
            showerror('错误', '已经是第一天了。', parent=self.winfo_toplevel())
            return
        self._de_date.set(self._market.date_handler.date)
        self._confirm_date()

    def _load_next(self):
        if self._market.next() == 1:
            showerror('错误', '已经是最后一天了。', parent=self.winfo_toplevel())
            return
        self._de_date.set(self._market.date_handler.date)
        self._confirm_date()
