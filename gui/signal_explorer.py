from gui.date_entry import *
from tkinter.messagebox import *
from gui.subwindow import *
from gui.listbox_search import ListboxSearcher
from gui.market_viewer import MarketViewer
from gui.stock_listbox import StockListbox
import tkinter as tk
from framework import InvestorTest


def _tw_insert(tw, values):
    tag = True
    for i in values:
        tw.insert('', 'end', values=i, tags=(str(tag),))
        tag = not tag
    tw.tag_configure('True', background='#E8E8E8')
    tw.tag_configure('False', background='#DFDFDF')


class SignalExplorer(ttk.Frame):
    def __init__(self, player, master, **kw):
        super().__init__(master, **kw)
        # 实例属性
        self._player = player
        self._market = player.market
        self._li_dates = list(self._player.strategy_history.keys())
        self._index = len(self._li_dates) - 1
        self._searching = False
        self._market_viewing = False
        # 界面设计
        self._fm_date_confirm = ttk.Frame(self)
        self._fm_date_confirm.pack(pady=5)
        self._lb_date = ttk.Label(self._fm_date_confirm, text='输入日期')
        self._lb_date.grid(row=0, column=0, sticky=tk.W, padx=8)
        self._de_date = DateEntry(self._fm_date_confirm)
        self._de_date.set(self._li_dates[-1])
        self._de_date.grid(row=1, column=0, padx=5)
        self._bt_goto = ttk.Button(self._fm_date_confirm, text='转到', command=self._confirm_date, width=5)
        self._bt_goto.grid(row=1, column=1, padx=5)
        self._str_date = tk.StringVar()
        self._lb_state = ttk.Label(self, textvariable=self._str_date, font=('黑体', 12))
        self._lb_state.pack(pady=5)
        self._nb_signal = ttk.Notebook(self)
        self._fm_signal_buy = ttk.Frame(self._nb_signal)
        self._lsb_buy = StockListbox(self._fm_signal_buy, width=23)
        self._lsb_buy.pack(side=tk.LEFT)
        self._scroll_buy = ttk.Scrollbar(self._fm_signal_buy)
        self._scroll_buy.config(command=self._lsb_buy.yview)
        self._lsb_buy.config(yscrollcommand=self._scroll_buy.set)
        self._scroll_buy.pack(side=tk.LEFT, fill=tk.Y)
        self._fm_signal_sell = ttk.Frame(self._nb_signal)
        self._lsb_sell = StockListbox(self._fm_signal_sell, width=23)
        self._lsb_sell.pack(side=tk.LEFT)
        self._scroll_sell = ttk.Scrollbar(self._fm_signal_sell)
        self._scroll_sell.config(command=self._lsb_sell.yview)
        self._lsb_sell.config(yscrollcommand=self._scroll_sell.set)
        self._scroll_sell.pack(side=tk.LEFT, fill=tk.Y)
        self._fm_signal_t = ttk.Frame(self._nb_signal)
        self._lsb_t = StockListbox(self._fm_signal_t, width=23)
        self._lsb_t.pack(side=tk.LEFT)
        self._scroll_t = ttk.Scrollbar(self._fm_signal_t)
        self._scroll_t.config(command=self._lsb_t.yview)
        self._lsb_t.config(yscrollcommand=self._scroll_t.set)
        self._scroll_t.pack(side=tk.LEFT, fill=tk.Y)
        self._nb_signal.add(self._fm_signal_buy)
        self._nb_signal.add(self._fm_signal_sell)
        self._nb_signal.add(self._fm_signal_t)
        self._fm_warehouse = None
        self._tw_warehouse = None
        self._scroll_warehouse = None
        self._bt_detail = None
        self._swnd_detail = None
        if type(player) != InvestorTest:
            style = ttk.Style()
            style.configure('Wre.Treeview', rowheight=40)
            style.configure('Wre.TButton', background='white')
            self._fm_warehouse = ttk.Frame(self._nb_signal)
            self._tw_warehouse = ttk.Treeview(self._fm_warehouse, show='headings', columns=('0', '1', '2', '3'))
            self._tw_warehouse.config(style='Wre.Treeview')
            self._tw_warehouse.heading('0', text='标的')
            self._tw_warehouse.heading('1', text='建仓时间')
            self._tw_warehouse.heading('2', text='盈亏')
            self._tw_warehouse.column('0', width=40)
            self._tw_warehouse.column('1', width=60)
            self._tw_warehouse.column('2', width=20)
            self._tw_warehouse.column('3', width=1)
            self._tw_warehouse.place(relx=0, rely=0, relwidth=1, relheight=1)
            self._scroll_warehouse = ttk.Scrollbar(self._tw_warehouse)
            self._scroll_warehouse.config(command=self._tw_warehouse.yview)
            self._tw_warehouse.config(yscrollcommand=self._scroll_warehouse.set)
            self._scroll_warehouse.place(relx=.9, rely=.14, relheight=.85)
            self._bt_detail = ttk.Button(self._fm_warehouse, text='展开', style='Wre.TButton')
            self._bt_detail.place(anchor=tk.CENTER, relx=.5, rely=.88)
            self._nb_signal.add(self._fm_warehouse)
        self._nb_signal.pack(pady=5)
        self._fm_date_button = ttk.Frame(self)
        self._fm_date_button.pack()
        self._bt_previous = ttk.Button(self._fm_date_button, text='前一天', command=self._load_previous)
        self._bt_previous.grid(row=0, column=0)
        self._bt_next = ttk.Button(self._fm_date_button, text='后一天', command=self._load_next)
        self._bt_next.grid(row=0, column=1)
        self._fm_option_button = ttk.Frame(self)
        self._fm_option_button.pack(pady=5)
        self._bt_copy_page = ttk.Button(self._fm_option_button, text='复制当前页', command=self._copy_page)
        self._bt_copy_page.grid(row=0, column=0)
        self._bt_copy_today = ttk.Button(self._fm_option_button, text='复制今天', command=self._copy_today)
        self._bt_copy_today.grid(row=0, column=1)
        self._bt_copy_all = ttk.Button(self._fm_option_button, text='复制每一天', command=self._copy_all)
        self._bt_copy_all.grid(row=1, column=0)
        self._bt_market_view = ttk.Button(self._fm_option_button, text='市场浏览', command=self._market_view)
        self._bt_market_view.grid(row=1, column=1)
        self._fm_search = ttk.Frame(self)
        self._fm_search.pack(pady=5)
        self._bt_search = ListboxSearcher(self._fm_search)
        self._bt_search.set_listbox([self._lsb_buy, self._lsb_sell, self._lsb_t])
        self._bt_search.set_prior_func(self._on_prior)
        self._bt_search.set_next_func(self._on_next)
        self._bt_search.grid(row=2, column=0, columnspan=2)
        self._tab = (('买入', '买入*'), ('卖出', '卖出*'), ('做T', '做T*'), ('持仓', '持仓*'))
        self._market_wnd = None
        self._confirm_date()

    def _confirm_date(self):
        date = self._de_date.get_datetime()
        if date is None:
            return
        if date not in self._player.strategy_history:
            showerror('错误', '{}-{}-{}不是交易日！'.format(*self._de_date.get()), parent=self.winfo_toplevel())
            return
        self._str_date.set('{}-{}-{}'.format(*self._de_date.get()))
        self._index = self._li_dates.index(date)
        sig = self._player.strategy_history[date]
        info = self._market.get_quotes(date)
        self._lsb_buy.set_info(info, self._player)
        self._lsb_buy.delete('0', 'end')
        self._lsb_buy.insert('end', *sig[0])
        self._lsb_sell.set_info(info, self._player)
        self._lsb_sell.delete('0', 'end')
        self._lsb_sell.insert('end', *sig[1])
        self._lsb_t.set_info(info, self._player)
        self._lsb_t.delete('0', 'end')
        self._lsb_t.insert('end', *sig[2])
        for i in range(3):
            if sig[i]:
                self._nb_signal.tab(i, text=self._tab[i][1])
            else:
                self._nb_signal.tab(i, text=self._tab[i][0])
        if type(self._player) != InvestorTest:
            items = self._tw_warehouse.get_children()
            for i in items:
                self._tw_warehouse.delete(i)
            warehouse = self._player.warehouse_history[date]
            if warehouse:
                self._nb_signal.tab(3, text=self._tab[3][1])
                _tw_insert(self._tw_warehouse, warehouse)

                def show_detail():
                    self._swnd_detail = SubWindow(self.winfo_toplevel())
                    self._swnd_detail.title(f'{date}的持仓')
                    self._swnd_detail.geometry('500x300')
                    tw = ttk.Treeview(self._swnd_detail, show='headings', columns=('0', '1', '2'))
                    tw.config(style='Wre.Treeview')
                    tw.heading('0', text='标的')
                    tw.heading('1', text='建仓时间')
                    tw.heading('2', text='盈亏')
                    tw.column('0', width=40)
                    tw.column('1', width=60)
                    tw.column('2', width=20)
                    tw.place(relx=0, rely=0, relwidth=1, relheight=1)
                    _tw_insert(tw, warehouse)
                self._bt_detail.config(command=show_detail)
            else:
                self._nb_signal.tab(3, text=self._tab[3][0])
        self._bt_search.search()

    def _load_previous(self):
        if self._index == 0:
            showerror('错误', '已经是第一天了。', parent=self.winfo_toplevel())
            return
        self._index -= 1
        self._de_date.set(self._li_dates[self._index])
        self._confirm_date()

    def _load_next(self):
        if self._index == len(self._li_dates) - 1:
            showerror('错误', '已经是最后一天了。', parent=self.winfo_toplevel())
            return
        self._index += 1
        self._de_date.set(self._li_dates[self._index])
        self._confirm_date()

    def _copy_page(self):
        current = self._nb_signal.index('current')
        page_name = self._nb_signal.tab(current, 'text')
        if page_name.startswith(self._tab[0][0]):
            content = self._lsb_buy.get('0', 'end')
        elif page_name.startswith(self._tab[1][0]):
            content = self._lsb_sell.get('0', 'end')
        else:
            content = self._lsb_t.get('0', 'end')
        if content:
            self.clipboard_clear()
            self.clipboard_append(str(content))
            showinfo('完成', '当前页内容已复制。', parent=self.winfo_toplevel())

    def _copy_today(self):
        self.clipboard_clear()
        self.clipboard_append('Buy:\n')
        self.clipboard_append(str(self._lsb_buy.get('0', 'end')) + '\n')
        self.clipboard_append('Sell:\n')
        self.clipboard_append(str(self._lsb_sell.get('0', 'end')) + '\n')
        self.clipboard_append('T:\n')
        self.clipboard_append(str(self._lsb_t.get('0', 'end')) + '\n')
        showinfo('完成', '今日内容已复制。', parent=self.winfo_toplevel())

    def _copy_all(self):
        self.clipboard_clear()
        self.clipboard_append(str(self._player.strategy_history))
        showinfo('完成', '全部内容已复制。', parent=self.winfo_toplevel())

    def _market_view(self):
        if self._market_viewing:
            self._market_wnd.focus()
            return
        self._market_viewing = True
        swnd = SubWindow(self.winfo_toplevel())
        self._market_wnd = swnd
        swnd.title('探索市场')
        swnd.geometry('260x360+{}+{}'.format(self.master.winfo_x(), self.master.winfo_y() + 30))
        old = self._market.ctime
        self._market.ctime = self._li_dates[self._index]
        mv = MarketViewer(self._player.market, swnd)
        self._market.ctime = old
        mv.set_player(self._player)
        mv.pack(fill=tk.BOTH, expand=True)
        self.wait_window(swnd)
        self._market_wnd = None
        self._market_viewing = False

    def _on_prior(self):
        if not self._bt_search.previous():
            return
        self._nb_signal.select(str(self._bt_search.get()[0]))

    def _on_next(self):
        if not self._bt_search.next():
            return
        self._nb_signal.select(str(self._bt_search.get()[0]))
