from gui.scene import Scene
from gui.thread_progress_bar import ThreadProgressBar
from gui.subwindow import SubWindow
from general_thread import *
from gui.signal_explorer import SignalExplorer
from framework import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import *
import random


class SceneRecommend(Scene):
    def __init__(self, master, **kw):
        super().__init__('今日发牌', master, **kw)
        self.bt_licensing = tk.Button(self, text='发牌!', command=self._licensing)
        self.bt_licensing.config(width=7, height=2, font=('等线', 12), relief='flat', cursor='hand2')
        self.bt_licensing.pack(pady=10)
        self.fm_card_count = ttk.Frame(self)
        self.fm_card_count.pack(pady=5)
        self.lb_count = ttk.Label(self.fm_card_count, text='发牌数：')
        self.lb_count.grid(row=0, column=0)
        self.spb_count = ttk.Spinbox(self.fm_card_count, from_=1, to=1000, width=5)
        self.spb_count.config(validate='all')
        self.spb_count.config(validatecommand=(self.register(self._verify_num), '%P'))
        self.spb_count.set(100)
        self.spb_count.grid(row=0, column=1)
        self._cfg = self.controller.setting
        self._flashing = False
        self.bind('<Map>', lambda x: self.start_flash())
        self.bind('<Unmap>', lambda x: self.stop_flash())
        self.bind('<Destroy>', lambda x: self.stop_flash())
        self._swnd = None
        self._listening = False
        self._color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self._r = 0
        self._g = 0
        self._b = 0

    @staticmethod
    def _verify_num(content):
        if content == '':
            return True
        if content.isdigit() and 1 <= int(content) <= 1000:
            return True
        return False

    def _licensing(self):
        if self._listening:
            self._swnd.focus()
            return
        try:
            chn = self._cfg.channel_loader.get_channel(self._cfg.channel)
            li_pool = self._cfg.pool_loader.get_pool(self._cfg.pool)
        except KeyError as e:
            showerror(str(type(e)), str(e))
            return
        self._listening = True
        swnd = SubWindow(self.root)
        self._swnd = swnd
        swnd.title('下载中')
        swnd.geometry('240x20')
        tpb = ThreadProgressBar(swnd)
        tpb.pack(fill=tk.X)
        d0 = Date()
        d1 = d0.date
        d0.add_days(-int(self.spb_count.get()))
        d2 = d0.date
        date_info = (d2, d1)
        td = MarketDownloader(chn, li_pool, date_info)
        td.set_callback(CallbackFactory.get_instance(td))
        tpb.load_thread(td)
        if td.code != 0:
            swnd.destroy()
            self._listening = False
            return
        swnd.title('加载中')
        res = td.res
        mkt = Market(datetime.datetime(*d2), datetime.datetime(*d1))
        if self._cfg.strategy_mode == 'vector':
            props = []
            for n in self._cfg.strategy:
                sp = self._cfg.strategy_loader.get_strategy(n)
                props.extend(sp.prop)
            td = MarkerLoader(mkt, res, props)
        else:
            td = MarkerLoader(mkt, res)
        td.set_callback(CallbackFactory.get_instance(td))
        tpb.load_thread(td)
        swnd.title('发牌中')
        li_stg = self._cfg.strategy
        if self._cfg.strategy_mode == 'vector':
            _li_stg = []
            group_buy = []
            group_sell = []
            for i in li_stg:
                sp = self._cfg.strategy_loader.get_strategy(i)
                if not _li_stg:
                    _li_stg.append(sp.func)
                group_buy.extend(sp.group_buy)
                group_sell.extend(sp.group_sell)
            td_sl = MarketSliceProcessor(mkt, group_buy, group_sell)
            tpb.load_thread(td_sl)
            if td_sl.code != 0:
                swnd.destroy()
                self._listening = False
                return
            li_stg = [lambda x: _li_stg[0](x, td_sl.res)] if _li_stg else []
        else:
            for i in range(len(li_stg)):
                li_stg[i] = self._cfg.strategy_loader.get_strategy(li_stg[i]).func
        player = InvestorTest(mkt)
        td = BacktestThread(player, li_stg)
        td.set_callback(CallbackFactory.get_instance(td))
        tpb.load_thread(td)
        tpb.destroy()
        swnd.title('发牌完毕·请查收')
        swnd.geometry('260x460')
        sie = SignalExplorer(player, swnd)
        sie.pack(ipady=10, fill=tk.BOTH, expand=True)
        self.wait_window(swnd)
        self._listening = False

    def start_flash(self):
        if self._flashing:
            return
        self._flashing = True
        self._flush()

    def stop_flash(self):
        self._flashing = False

    def _flush(self):
        if self._flashing:
            color = random.randint(0, (1 << 24) - 1)
            mask = (1 << 8) - 1
            r, g, b = (color & (mask << 16)) >> 16, (color & (mask << 8)) >> 8, color & mask
            self.bt_licensing.config(bg='#{:06X}'.format(color))
            if r + g + b > 300 and r + g > 200 and g > 100:
                self.bt_licensing.config(fg='black')
            else:
                self.bt_licensing.config(fg='GhostWhite')
            self._r, self._g, self._b = self._color
            self._toggle(self._color, (r, g, b))
            self._color = (r, g, b)
            self.after(1000, self._flush)

    def _toggle(self, src: tuple[int, int, int], dst: tuple[int, int, int]):
        if self._flashing:
            frame = 60
            in_r = dst[0] - src[0]
            in_g = dst[1] - src[1]
            in_b = dst[2] - src[2]
            self._transfer(in_r / frame, in_g / frame, in_b / frame, frame)

    def _transfer(self, ir, ig, ib, frame):
        if frame <= 0:
            return
        if self._flashing:
            self._r += ir
            if self._r > 255:
                self._r = 255
            if self._r < 0:
                self._r = 0
            self._g += ig
            if self._g > 255:
                self._g = 255
            if self._g < 0:
                self._g = 0
            self._b += ib
            if self._b > 255:
                self._b = 255
            if self._b < 0:
                self._b = 0
            self.bt_licensing.config(bg=f'#{int(self._r):02X}{int(self._g):02X}{int(self._b):02X}')
            self.bt_licensing.update_idletasks()
            self.after(10, lambda: self._transfer(ir, ig, ib, frame - 1))
