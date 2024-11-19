from gui.date_interval_entry import DateIntervalEntry
from gui.scene import Scene, SceneSetting
from gui.signal_explorer import _tw_insert
from gui.stdguiio import StdGuiIO
from gui.check_board import *
from gui.signal_explorer import *
from general_thread import *
from gui.thread_progress_bar import *
from framework import *
import backtest
from tools import *
from tkinter.filedialog import asksaveasfilename
import csv


class SceneBacktest(Scene):
    def __init__(self, master, **kw):
        super().__init__('策略回测', master, **kw)
        # 界面设计
        self.date_entry = DateIntervalEntry(self)
        self.date_entry.pack(expand=True)
        self.fm_progress = ttk.Frame(self)
        self.fm_progress.pack(pady=10)
        self.progressbar = ThreadProgressBar(self.fm_progress)
        self.progressbar.pack(fill=tk.X)
        self.stdio = StdGuiIO(self.fm_progress, width=28, height=8, bg='#2B2B2B', fg='#A2AAAC')
        self.stdio.pack()
        self.fm_option_button = ttk.Frame(self)
        self.fm_option_button.pack(pady=5)
        self.bt_start_test = ttk.Button(self.fm_option_button, text='开始回测', command=self._start_test)
        self.bt_start_test.config(width=8)
        self.bt_start_test.grid(row=0, column=0, padx=1, ipady=2)
        self.bt_update_data = ttk.Button(self.fm_option_button, text='更新数据', command=self.update_data)
        self.bt_update_data.config(width=8)
        self.bt_update_data.grid(row=0, column=1, padx=1, ipady=2)
        self.bt_explor_market = ttk.Button(self.fm_option_button, text='市场浏览', command=self._explor_market)
        self.bt_explor_market.config(width=8)
        self.bt_explor_market.grid(row=0, column=2, padx=1, ipady=2)
        self.fm_result_button = ttk.Frame(self)
        self.fm_result_button.pack()
        # 实例属性
        self._cfg = self.controller.setting
        self._pool = None
        self._market: Market | None = None
        self._player: Investor | None = None
        self._fig = [None, None, None]
        self._vec_sp = None
        self._sp_func = None
        self._sp_func_pack = None
        self._mode = self._cfg.strategy_mode
        # 初始化
        self.bind('<Map>', self._update_config)
        self.bind('<Unmap>', self._stop_download)
        self.bind('<Destroy>', self._stop_download)
        self.date_entry.de_start_time.set((2015, 1, 1))
        self.date_entry.de_end_time.set(Date().date)
        # 回测数据记录
        self._value = 0
        self._win_rate = 0
        self._sum_inc = 0
        self._max_lose = 0
        self._max_inc = 0
        self._max_down = 0
        self._avg_lose = 0
        self._avg_inc = 0
        self._mid_lose = 0
        self._mid_inc = 0
        self._exp_inc = 0

    def _stop_download(self, event):
        if event.widget != self:
            return
        backtest.plt.close('all')

    def _update_config(self, event):
        if event.widget != self:
            return
        pool = self._cfg.pool
        if pool in CommonPool.refer:
            pool = pool.replace('*', '').strip()
        if (
            self._cfg.strategy_mode != self._mode or
            self._pool != pool or
            (
                self._cfg.strategy_mode == 'vector' and
                self._vec_sp is not None and self._vec_sp != self._cfg.strategy
            )
        ):
            self.stdio.clear()
            self.stdio.write('loading data..\n')
            r = self._load()
            if r is None:
                self.stdio.write('load completed.\n')
            elif r == 1:
                self.stdio.write('load failed.\n')
        self._mode = self._cfg.strategy_mode

    def _load(self):
        pool = self._cfg.pool
        if pool in CommonPool.refer:
            pool = pool.replace('*', '').strip()
        pool_path = '../data/' + pool
        if not (path.exists(pool_path) and path.exists(pool_path + '/' + 'date_info.pkl')):
            self.bell()
            act = askyesno('获取数据', '没有找到数据包%s。\n要获取吗？' % self._cfg.pool, parent=self.root)
            if act:
                date_info = self.date_entry.get()
                if date_info is None:
                    return 1
                if self._download_market(date_info) == 1:
                    showerror('错误', '获取失败。')
                    return 1
                else:
                    self.stdio.write('loading data..\n')
            else:
                return 2
        self._load_market()

    def _load_market(self):
        pool = self._cfg.pool
        if pool in CommonPool.refer:
            pool = pool.replace('*', '').strip()
        pool_path = '../data/' + pool + '/'
        date_info = load_pkl(pool_path + 'date_info.pkl')
        stime = datetime.datetime(*date_info[0])
        ctime = datetime.datetime(*date_info[1])
        self._market = Market(stime, ctime)
        if SceneSetting.get_instance().strategy_mode == 'vector':
            props = []
            for n in SceneSetting.get_instance().strategy:
                sp = SceneSetting.get_instance().strategy_loader.get_strategy(n)
                props.extend(sp.prop)
            if not props:
                td = MarkerLoader(self._market, pool_path)
            else:
                td = MarkerLoader(self._market, pool_path, props)
        else:
            td = MarkerLoader(self._market, pool_path)
        td.set_callback(CallbackFactory.get_instance(td))
        self.progressbar.load_thread(td)
        self._pool = pool
        self.date_entry.set(*date_info)
        if not self._cfg.strategy_mode == 'vector':
            return
        self._vec_sp = self._cfg.strategy
        self._sp_func = self._sp_func_pack = None

    def _download_market(self, date_info):
        pool = self._cfg.pool
        try:
            li_pool = self._cfg.pool_loader.get_pool(pool)
            chn = self._cfg.channel_loader.get_channel(self._cfg.channel)
        except KeyError as e:
            showinfo(str(type(e)), str(e))
            return 1
        self.stdio.write('downloading data..\n')
        td_download = MarketDownloader(chn, li_pool, date_info)
        td_download.set_callback(CallbackFactory.get_instance(td_download))
        self.progressbar.load_thread(td_download)
        if td_download.res is None:
            self.stdio.write('download failed.\n')
            return 1
        res = td_download.res
        self.stdio.write('download completed.\n')
        self.stdio.write('writing data..\n')
        if pool in CommonPool.refer:
            pool = pool.replace('*', '').strip()
        save_path = '../data/' + pool + '/'
        td_write = MarketWriter(li_pool, res, save_path)
        td_write.set_callback(CallbackFactory.get_instance(td_write))
        self.progressbar.load_thread(td_write)
        self.stdio.write('write completed.\n')

    def update_data(self):
        if self.progressbar.is_running():
            showwarning('警告', '请先等待程序执行完毕。', parent=self.root)
            return 2
        pool = self._cfg.pool
        date_info = self.date_entry.get()
        if date_info is None:
            return 1
        self.bell()
        act = askyesno(
            '更新数据',
            '是否更新数据？\n\n频道: {}\n股票池: {}\n开始时间: {}\n结束时间: {}'.format(self._cfg.channel, pool, *date_info),
            parent=self.root
        )
        if act:
            self.stdio.clear()
            r = self._download_market(date_info)
            if r == 1:
                showerror('错误', '获取失败。')
                return 1
            self.stdio.write('loading data..\n')
            self._load_market()
            self.stdio.write('load completed.\n')
            self.stdio.write('update completed.\n')

    def _start_test(self):
        if self.progressbar.is_running():
            showwarning('警告', '请先等待程序执行完毕。', parent=self.root)
            return 2
        pool = self._cfg.pool
        date_info = self.date_entry.get()
        if date_info is None:
            return 1
        dsc = '是否执行数据包\n{}\n从{}到{}的回测？\n\n加载的策略有：\n'.format(pool, *date_info)
        dsc += '\n'.join(self._cfg.strategy)
        self.bell()
        act = askyesno('回测', dsc, parent=self.root)
        if not act:
            return
        if pool in CommonPool.refer:
            pool = pool.replace('*', '').strip()
        pool_path = '../data/' + pool
        true_date_info = load_pkl(pool_path + '/' + 'date_info.pkl')
        if date_info[0] < true_date_info[0] or date_info[1] > true_date_info[1]:
            showwarning('警告', '超出数据记录的有效日期\n{}-{}。'.format(*true_date_info), parent=self.root)
        self._market.stime = datetime.datetime(*date_info[0])
        self._market.ctime = datetime.datetime(*date_info[1])
        self._market.remake()
        li_stg = self._cfg.strategy
        group_buy = []
        group_sell = []
        if self._cfg.strategy_mode == 'vector':
            _li_stg = []
            for i in li_stg:
                sp = self._cfg.strategy_loader.get_strategy(i)
                if not _li_stg:
                    _li_stg.append(sp.func)
                group_buy.extend(sp.group_buy)
                group_sell.extend(sp.group_sell)
            if _li_stg:
                if self._sp_func is not _li_stg[0]:
                    self.stdio.clear()
                    self.stdio.write('signal sending..\n')
                    td_sl = MarketSliceProcessor(self._market, group_buy, group_sell)
                    self.progressbar.load_thread(td_sl)
                    if td_sl.code != 0:
                        return
                    self.stdio.write('signal sent already.\n')
                    self._sp_func = _li_stg[0]
                    self._sp_func_pack = lambda x: self._sp_func(x, td_sl.res)
                li_stg = [self._sp_func_pack]
        else:
            for i in range(len(li_stg)):
                li_stg[i] = self._cfg.strategy_loader.get_strategy(li_stg[i]).func
            # if li_stg:
            #     self.stdio.clear()
            #     self.stdio.write('signal sending..\n')
            #     td_sl = CommonMarketSliceProcessor(self._market, li_stg, self._cfg.strategy_loader)
            #     self.progressbar.load_thread(td_sl)
            #     if td_sl.code != 0:
            #         return
            #     self.stdio.write('signal sent already.\n')
            #     print(td_sl.res)
        self.stdio.clear()
        self.stdio.write('backtesting..\n')
        self._player = InvestorChina(self._market)
        td_load = BacktestThread(self._player, li_stg)
        td_load.set_callback(CallbackFactory.get_instance(td_load))
        self.progressbar.load_thread(td_load)
        if td_load.code != 0:
            return
        # 读取回测统计
        value = self._player.value
        win_rate = self._player.win_rate
        sum_inc = self._player.get_income_rate()
        max_win = self._player.max_win
        max_lose = self._player.max_lose
        max_down = self._player.max_down
        avg_win = self._player.avg_win
        avg_lose = self._player.avg_lose
        mid_win = self._player.mid_win
        mid_lose = self._player.mid_lose
        exp_inc = self._player.exp_inc
        # 显示信息
        self.stdio.write('backtest completed.\n')
        self.stdio.write('单位净值:  {}  {}\n'.format(self._player.get_value(), self._get_udc(value, '_value')))
        self.stdio.write('胜率:       {:.2f} %  {}\n'.format(win_rate * 100, self._get_udc(win_rate, '_win_rate')))
        self.stdio.write('累计收益率: {:.4f}  {}\n'.format(sum_inc, self._get_udc(sum_inc, '_sum_inc')))
        self.stdio.write('最大正收益: {:.2f} %  {}\n'.format(max_win * 100, self._get_udc(max_win, '_max_inc')))
        self.stdio.write('最大负收益: {:.2f} %  {}\n'.format(max_lose * 100, self._get_udc(max_lose, '_max_lose')))
        self.stdio.write('最大回撤: {:.2f} %  {}\n'.format(max_down * 100, self._get_udc(max_down, '_max_down')))
        self.stdio.write('平均正收益: {:.2f} %  {}\n'.format(avg_win * 100, self._get_udc(avg_win, '_avg_inc')))
        self.stdio.write('平均负收益: {:.2f} %  {}\n'.format(avg_lose * 100, self._get_udc(avg_lose, '_avg_lose')))
        self.stdio.write('中位正收益: {:.2f} %  {}\n'.format(mid_win * 100, self._get_udc(mid_win, '_mid_inc')))
        self.stdio.write('中位负收益: {:.2f} %  {}\n'.format(mid_lose * 100, self._get_udc(mid_lose, '_mid_lose')))
        self.stdio.write('预期收益率: {:.2f} %  {}\n'.format(exp_inc * 100, self._get_udc(exp_inc, '_exp_inc')))
        span, sincr = self._player.best_span()
        self.stdio.write('最佳周期-收益：{}-{:.2f} % '.format(span, sincr * 100))
        # 更新记录
        self._value, self._win_rate, self._sum_inc, self._max_down = value, win_rate, sum_inc, max_down
        self._max_inc, self._max_lose, self._avg_inc, self._avg_lose = max_win, max_lose, avg_win, avg_lose
        self._mid_inc, self._mid_lose, self._exp_inc = mid_win, mid_lose, exp_inc
        # 添加查看按钮
        bt_draw_plt = ttk.Button(self.fm_result_button, text='绘制图表', command=self._draw_plt)
        bt_draw_plt.grid(row=0, column=0, padx=2)
        bt_history = ttk.Button(self.fm_result_button, text='查看操作记录', command=self._inquire_history)
        bt_history.grid(row=0, column=1, padx=2)

    def _get_udc(self, value, prop):
        ref = self.__getattribute__(prop)
        if value > ref:
            return '/\\'
        elif value < ref:
            return '\\/'
        return ''

    def _draw_plt(self):
        self.disable()
        swnd = SubWindow(self.root)
        swnd.title('确认绘制项')
        ckb = CheckBoard(swnd)
        ckb.append('持仓收益率')
        ckb.append('累计收益率')
        ckb.append('单位净值')
        ckb.append('操作记录')
        ckb.pack(fill=tk.BOTH, expand=True)
        option = []

        def confirm():
            li = ckb.get_true()
            option.extend(li)
            swnd.destroy()

        fm_confirm = ttk.Frame(swnd)
        fm_confirm.pack(fill=tk.BOTH, expand=True)
        bt_confirm = ttk.Button(fm_confirm, text='确认', command=confirm)
        bt_confirm.pack()
        self.wait_window(swnd)
        self.enable()
        if not option:
            return
        backtest.plt.rcParams['font.family'] = 'Arial'
        for i in option:
            match i:
                case '持仓收益率':
                    fig = backtest.draw_warehouse_income(self._player)
                    self._fig[0] = fig
                    fig.canvas.mpl_connect('close_event', lambda x: self._clear_fig(0))
                case '累计收益率':
                    fig = backtest.draw_grant_income(self._player)
                    self._fig[1] = fig
                    fig.canvas.mpl_connect('close_event', lambda x: self._clear_fig(1))
                case '单位净值':
                    fig = backtest.draw_unit_worth(self._player)
                    self._fig[2] = fig
                    fig.canvas.mpl_connect('close_event', lambda x: self._clear_fig(2))
                case '操作记录':
                    swnd = tk.Toplevel(self.winfo_toplevel())
                    swnd.title('操作记录')
                    swnd.geometry('800x400')
                    tw = ttk.Treeview(swnd, show='headings', columns=('0', '1', '2', '3', '4', '5'))
                    tw.heading('0', text='标的')
                    tw.heading('1', text='建仓时间')
                    tw.heading('2', text='持仓周期')
                    tw.heading('3', text='最大收益')
                    tw.heading('4', text='最大回撤')
                    tw.heading('5', text='收益率')
                    tw.column('0', width=100)
                    tw.column('1', width=100)
                    tw.column('2', width=100)
                    tw.column('3', width=100)
                    tw.column('4', width=100)
                    tw.column('5', width=100)
                    tw.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
                    scb = ttk.Scrollbar(swnd)
                    scb.config(command=tw.yview)
                    tw.config(yscrollcommand=scb.set)
                    scb.pack(fill=tk.Y, side=tk.LEFT)
                    _tw_insert(tw, self._player.history_operate)

                    def call_menu(event):
                        mb = tk.Menu(tw, tearoff=0)
                        mb.add_command(label='导出为CSV', command=lambda: self._export_csv(swnd))
                        mb.post(event.x_root, event.y_root)
                    tw.bind('<Button-3>', call_menu)
        PlotThread.update()

    def _export_csv(self, parent):
        file_path = asksaveasfilename(
            defaultextension='.csv', filetypes=[('Comma-Separated Values Files', '.csv')], initialfile='recoder.csv',
            parent=parent
        )
        if file_path.strip() == '':
            return
        with open(file_path, 'w', encoding='utf-8', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerows(self._player.history_operate)
        showinfo('完成', '导出成功', parent=parent)

    def _clear_fig(self, num):
        self._fig[num] = None

    def _inquire_history(self):
        self.disable()
        swnd = SubWindow(self.root)
        swnd.title('操作记录')
        swnd.geometry('260x460')
        sie = SignalExplorer(self._player, swnd)
        sie.pack(ipady=10, fill=tk.BOTH, expand=True)
        self.wait_window(swnd)
        self.enable()

    def _explor_market(self):
        if self.progressbar.is_running():
            showwarning('警告', '请先等待程序执行完毕。', parent=self.root)
            return 2
        self.disable()
        swnd = SubWindow(self.root)
        swnd.title('探索市场')
        swnd.geometry('260x360')
        mv = MarketViewer(self._market, swnd)
        mv.pack(fill=tk.BOTH, expand=True)
        self.wait_window(swnd)
        self.enable()

    def disable(self):
        """禁用按钮功能"""
        for w in self.fm_option_button.children.values():
            if isinstance(w, ttk.Button):
                w.config(state='disabled')
        for w in self.fm_result_button.children.values():
            if isinstance(w, ttk.Button):
                w.config(state='disabled')
        self.controller.disable()

    def enable(self):
        """启用按钮功能"""
        for w in self.fm_option_button.children.values():
            if isinstance(w, ttk.Button):
                w.config(state='normal')
        for w in self.fm_result_button.children.values():
            if isinstance(w, ttk.Button):
                w.config(state='normal')
        self.controller.enable()
