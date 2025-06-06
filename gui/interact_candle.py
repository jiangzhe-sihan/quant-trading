import mplfinance as mpf
import pandas
from matplotlib.widgets import MultiCursor


title_font = {
    'fontname': 'SimHei',
    'size': '16',
    'color': 'black',
    'weight': 'bold',
    'va': 'bottom',
    'ha': 'center'
}
large_red_font = {
    'fontname': 'Arial',
    'size': '20',
    'color': 'red',
    'weight': 'bold',
    'va': 'bottom',
}
large_green_font = {
    'fontname': 'Arial',
    'size': '20',
    'color': 'green',
    'weight': 'bold',
    'va': 'bottom',
}
small_red_font = {
    'fontname': 'Arial',
    'size': '12',
    'color': 'red',
    'weight': 'bold',
    'va': 'bottom',
}
small_green_font = {
    'fontname': 'Arial',
    'size': '12',
    'color': 'green',
    'weight': 'bold',
    'va': 'bottom',
}
normal_label_font = {
    'fontname': 'SimHei',
    'size': '12',
    'color': 'black',
    'va': 'bottom',
    'ha': 'right'
}
normal_font = {
    'fontname': 'Arial',
    'size': '12',
    'color': 'black',
    'va': 'bottom',
    'ha': 'right'
}
normal_font_left = {
    'fontname': 'SimHei',
    'size': '12',
    'color': 'black',
    'va': 'bottom',
    'ha': 'left'
}


def draw_kline(candle, adp, date, symbol, slist, signal=None, style=None):
    if style is None:
        mc = mpf.make_marketcolors(
            up='forestgreen',
            down='crimson',
            edge='inherit',
            wick='inherit',
            volume='inherit',
            inherit=True,
        )
        style = mpf.make_mpf_style(
            gridaxis='horizontal',
            gridstyle='-.',
            marketcolors=mc,
            rc={'font.family': 'SimHei'}
        )
    return InterCandle(candle, style, symbol, signal, date, adp, slist)


class InterCandle:  # 定义一个交互K线图类
    def __init__(self, data: pandas.DataFrame, my_style, symbol, signal, ctime, adp, parent):
        # 初始化交互式K线图对象，历史数据作为唯一的参数用于初始化对象
        self.data = data.join(adp)
        self.symbol = symbol
        self.style = my_style
        self._signal = signal
        self._insert_signal()
        self.adp = adp
        self._parent = parent
        # 设置初始化的K线图显示区间起点为0，即显示第0到第99个交易日的数据（前100个数据）
        idx = self.data.index.get_loc(ctime) if ctime in self.data.index else 0
        self.idx_start = idx if idx > 30 else 30 if len(data) >= 30 else len(data) - 1
        # 控制K线图的显示范围大小
        self.idx_range = 100 if self.idx_start >= 100 else self.idx_start
        self._min_range = 30 if self.idx_range > 30 else self.idx_range
        # 鼠标按键状态，False为按键未按下，True为按键按下
        self.pressed = False
        self.locked = False
        # 鼠标按下时的x坐标
        self.xpress = None
        # 相对移动距离
        self._dx = 0
        # 标记图像窗口是否关闭
        self._closed = False
        # 初始化figure对象，在figure上建立三个Axes对象并分别设置好它们的位置和基本属性
        self._fig = mpf.figure(style=my_style, figsize=(10, 7), facecolor=(0.82, 0.83, 0.85))
        fig = self._fig
        self._ax_price = fig.add_axes([0.08, 0.25, 0.88, 0.6])
        self._ax_volume = fig.add_axes([0.08, 0.10, 0.88, 0.15], sharex=self._ax_price)
        self._hline = None
        self._vline = None
        self._vline1 = None
        self._text_price = None
        self._xp = 0
        # 初始化figure对象，在figure上预先放置文本并设置格式，文本内容根据需要显示的数据实时更新
        # 初始化时，所有的价格数据都显示为空字符串
        self._tx_title = fig.text(0.50, 0.94, symbol, **title_font)
        self._tx_open_close_label = fig.text(0.12, 0.90, '开/收: ', **normal_label_font)
        self._tx_open_close_value = fig.text(0.14, 0.89, '', **large_red_font)
        self._tx_change = fig.text(0.14, 0.86, '', **small_red_font)
        self._tx_pct_change = fig.text(0.22, 0.86, '', **small_red_font)
        self._tx_date = fig.text(0.12, 0.86, '', **normal_label_font)
        self._tx_high_label = fig.text(0.40, 0.90, '高: ', **normal_label_font)
        self._tx_high_value = fig.text(0.40, 0.90, '', **small_red_font)
        self._tx_low_label = fig.text(0.40, 0.86, '低: ', **normal_label_font)
        self._tx_low_value = fig.text(0.40, 0.86, '', **small_green_font)
        self._tx_volume_label = fig.text(0.55, 0.90, '量: ', **normal_label_font)
        self._tx_volume_value = fig.text(0.55, 0.90, '', **normal_font_left)
        self._tx_last_close_label = fig.text(0.55, 0.86, '昨收: ', **normal_label_font)
        self._tx_last_close_value = fig.text(0.55, 0.86, '', **normal_font_left)
        self._tx_amount_label = fig.text(0.70, 0.90, '额: ', **normal_label_font)
        self._tx_amount_value = fig.text(0.70, 0.90, '', **normal_font_left)
        self._tx_hs_label = fig.text(0.70, 0.86, '换手: ', **normal_label_font)
        self._tx_hs_value = fig.text(0.70, 0.86, '', **normal_font_left)
        self._tx_lz_label = fig.text(0.85, 0.90, '流值: ', **normal_label_font)
        self._tx_lz_value = fig.text(0.85, 0.90, '', **normal_font_left)
        # 添加十字光标
        self._cursor = MultiCursor(self._fig.canvas,
                                   [self._ax_price, self._ax_volume],
                                   horizOn=True, color='gray', lw=1)
        # 鼠标按下事件与self.on_press回调函数绑定
        self._fig.canvas.mpl_connect('button_press_event', self.on_press)
        # 鼠标按键释放事件与self.on_release回调函数绑定
        self._fig.canvas.mpl_connect('button_release_event', self.on_release)
        # 鼠标移动事件与self.on_motion回调函数绑定
        self._fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        # 将新增的回调函数on_scroll与鼠标滚轮事件绑定起来
        self._fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        # 绑定关闭函数
        self._fig.canvas.mpl_connect('close_event', self.close)
        # self.refresh_plot()
        self._ax_price.clear()
        self._ax_volume.clear()
        self.refresh_texts(self.data.iloc[self.idx_start])
        self.refresh_plot()

    def _insert_signal(self):
        if 'buy' in self.data:
            return
        if self._signal is not None:
            self.data.insert(0, 'buy', None)
            self.data.insert(0, 'sell', None)
            self.data.insert(0, 't', None)
            for k, v in self._signal.iterrows():
                self.data.loc[k, 'buy'] = v['buy']
                self.data.loc[k, 'sell'] = v['sell']
                self.data.loc[k, 't'] = v['t']

    def refresh_plot(self, idx_start=None, idx_range=None):
        """ 根据最新的参数，重新绘制整个图表
        """
        self._hline = self._vline = self._vline1 = self._text_price = None
        if idx_start is None:
            idx_start = self.idx_start
        if idx_range is None:
            idx_range = self.idx_range
        plot_data = self.data.iloc[idx_start - idx_range:idx_start + 1]
        if idx_range < 200:
            ap = [mpf.make_addplot(plot_data[self.adp.columns], ax=self._ax_price, width=1)]
            if self._signal is not None:
                ap.append(
                    mpf.make_addplot(
                        plot_data['buy'],
                        ax=self._ax_price,
                        scatter=True,
                        marker='^',
                        color='g'
                    )
                )
                ap.append(
                    mpf.make_addplot(
                        plot_data['sell'],
                        ax=self._ax_price,
                        scatter=True,
                        marker='v',
                        color='r'
                    )
                )
                ap.append(
                    mpf.make_addplot(
                        plot_data['t'],
                        ax=self._ax_price,
                        scatter=True,
                        marker='*',
                        color='y'
                    )
                )
            mpf.plot(plot_data,
                     ax=self._ax_price,
                     volume=self._ax_volume,
                     addplot=ap,
                     type='candle',
                     style=self.style,
                     datetime_format='%Y-%m-%d',
                     xrotation=0)
        else:
            mpf.plot(plot_data,
                     ax=self._ax_price,
                     volume=self._ax_volume,
                     type='line',
                     style=self.style,
                     datetime_format='%Y-%m-%d',
                     xrotation=0)
        self._fig.canvas.draw_idle()
        self._fig.canvas.flush_events()
        if not self._closed:
            self._fig.show()

    @staticmethod
    def _format_num(num):
        if num // 100000000:
            num = f'{num / 100000000:.2f}亿'
        elif num // 10000:
            num = f'{num / 10000:.2f}万'
        return num

    def refresh_texts(self, display_data):
        """ 更新K线图上的价格文本
        """
        # display_data是一个交易日内的所有数据，将这些数据分别填入figure对象上的文本中
        self._tx_open_close_value.set_text(f'{display_data["open"]} / {display_data["close"]}')
        self._tx_change.set_text(f'{display_data["change"]:.3f}')
        self._tx_pct_change.set_text(f'[{display_data["pct_change"]:.2f}%]')
        self._tx_date.set_text(f'{display_data.name.date()}')
        self._tx_high_value.set_text(f'{display_data["high"]}')
        self._tx_low_value.set_text(f'{display_data["low"]}')
        self._tx_volume_value.set_text(f'{display_data["volume"]:.0f}')
        self._tx_last_close_value.set_text(f'{display_data["last_close"]}')
        amount = display_data["amount"]
        self._tx_amount_value.set_text(f'{self._format_num(amount)}')
        self._tx_hs_value.set_text(f'{display_data["hs"]}')
        lz = display_data["lz"]
        self._tx_lz_value.set_text(f'{self._format_num(lz)}')
        # 根据本交易日的价格变动值确定开盘价、收盘价的显示颜色
        if display_data['change'] > 0:  # 如果今日变动额大于0，即今天价格高于昨天，今天价格显示为绿色
            close_number_color = 'green'
        elif display_data['change'] < 0:  # 如果今日变动额小于0，即今天价格低于昨天，今天价格显示为红色
            close_number_color = 'red'
        else:
            close_number_color = 'black'
        self._tx_open_close_value.set_color(close_number_color)
        self._tx_change.set_color(close_number_color)
        self._tx_pct_change.set_color(close_number_color)

    def _get_cur_idx(self, xp):
        if xp < 0:
            xp = 0
        elif xp > self.idx_range:
            xp = self.idx_range
        idx = self.idx_start - self.idx_range + xp
        return xp, idx

    def _arm_to_pos(self, x):
        x, idx = self._get_cur_idx(x)
        y = self.data.iloc[idx]['close']
        price_pos = self.idx_range + 1
        if self._vline is None:
            self._vline = self._ax_price.axvline(x, color='gray', lw=1)
            self._vline1 = self._ax_volume.axvline(x, color='gray', lw=1)
        else:
            self._vline.set_xdata([x])
            self._vline1.set_xdata([x])
        if self._hline is None:
            self._hline = self._ax_price.axhline(y, color='gray', lw=1)
        else:
            self._hline.set_ydata([y])
        if self._text_price is None:
            self._text_price = self._ax_price.text(price_pos, y, f'{y}', backgroundcolor='lightgray')
        else:
            self._text_price.set_position((price_pos, y))
            self._text_price.set_text(f'{y}')
        self.refresh_texts(self.data.iloc[idx])

    def on_press(self, event):
        # 当鼠标按键按下时，调用该函数，event为事件信息，是一个dict对象，包含事件相关的信息
        # 如坐标、按键类型、是否在某个Axes对象内等等
        # event.inaxes可用于判断事件发生时，鼠标是否在某个Axes内，在这里我们指定，只有鼠
        # 标在ax1内时，才能平移K线图，否则就退出事件处理函数
        if not event.inaxes == self._ax_price:
            return
        # 记录鼠标按下时的x坐标
        self.xpress = event.xdata
        # 检查是否按下了鼠标左键，如果不是左键，同样退出事件处理函数
        if event.button == 1:
            if self.locked:
                if event.dblclick:
                    self._parent.show_evaluate(
                        self.symbol,
                        self._parent.market.get_quotes(self.data.index[self._get_cur_idx(self._xp)[1]]),
                        self._fig.canvas.get_tk_widget().winfo_toplevel()
                    )
                return
            # 如果鼠标在ax1范围内，且按下了左键，条件满足，设置鼠标状态为pressed
            self.pressed = True
            # 退出函数，等待鼠标移动事件发生
            self._cursor.disconnect()
        elif event.button == 3:
            if self.pressed:
                return
            if self.locked:
                self._cursor.connect()
                self._update_idx()
                self._update_axes()
            else:
                self._cursor.disconnect()
                self._xp = int(round(self.xpress))
                self._arm_to_pos(self._xp)
            self._fig.canvas.draw_idle()
            self._fig.canvas.flush_events()
            self.locked = not self.locked

    # 鼠标移动事件处理
    def on_motion(self, event):
        # 如果鼠标按键没有按下pressed == False，则什么都不做，退出处理函数
        if not self.pressed:
            return
        if self.locked:
            return
        # 如果移动出了ax1的范围，也退出处理函数
        if not event.inaxes == self._ax_price:
            self.idx_start -= self._dx
            f = -1 if self._dx < 0 else 1
            self._dx = f * self.idx_range // self._min_range
            self._update_idx()
            self._update_axes()
            return
        # 如果鼠标在ax1范围内，且左键按下，则开始计算dx，并根据dx计算新的K线图起点
        self._dx = int(event.xdata - self.xpress)
        # 前面介绍过了，新的起点N(new) = N - dx
        new_idx = self.idx_start - self._dx
        # 设定平移的左右界限，如果平移后超出界限，则不再平移
        if new_idx >= len(self.data) - 1:
            new_idx = len(self.data) - 1
        if new_idx - self.idx_range < 0:
            new_idx = self.idx_range
        # 清除各个图表Axes中的内容，准备以新的起点重新绘制
        self._ax_price.clear()
        self._ax_volume.clear()
        # 更新图表上的文字、以新的起点开始绘制K线图
        self.refresh_texts(self.data.iloc[new_idx])
        self.refresh_plot(new_idx)

    # 鼠标按键释放
    def on_release(self, event):
        if self.locked:
            return
        # 按键释放后，设置鼠标的pressed为False
        if event.button != 1:
            return
        self.pressed = False
        self.idx_start -= self._dx
        self._dx = 0
        self._update_idx()
        self._update_axes()
        self._cursor.connect()

    def _update_idx(self):
        # 更新起始位置
        if self.idx_start >= len(self.data) - 1:
            self.idx_start = len(self.data) - 1
        if self.idx_start - self.idx_range < 0:
            self.idx_start = self.idx_range

    def _update_axes(self, with_text=True):
        # 清除各个图表Axes中的内容，准备以新的起点重新绘制
        self._ax_price.clear()
        self._ax_volume.clear()
        # 更新图表上的文字、以新的起点开始绘制K线图
        if with_text:
            self.refresh_texts(self.data.iloc[self.idx_start])
        self.refresh_plot()

    def on_scroll(self, event):
        if self.locked:
            if event.button == 'up':
                self._xp -= 1
                if self._xp < 0:
                    self._xp = 0
                    self.idx_start -= 1
                    self._update_idx()
                    self._update_axes(False)
            elif event.button == 'down':
                self._xp += 1
                if self._xp > self.idx_range:
                    self._xp = self.idx_range
                    self.idx_start += 1
                    self._update_idx()
                    self._update_axes(False)
            else:
                return
            self._arm_to_pos(self._xp)
            self._fig.canvas.draw_idle()
            self._fig.canvas.flush_events()
            return
        # 仅当鼠标滚轮在axes1范围内滚动时起作用
        if event.inaxes != self._ax_price:
            return
        if event.button == 'up':
            # 缩小20%显示范围
            scale_factor = 0.8
        elif event.button == 'down':
            # 放大20%显示范围
            scale_factor = 1.2
        else:
            scale_factor = 1
        # 设置K线的显示范围大小
        self.idx_range = int(self.idx_range * scale_factor)
        # 限定可以显示的K线图的范围，最少不能少于30个交易日，最大不能超过数据长度
        # K线数据总长度的差
        data_length = 300 if self.idx_start >= 300 else self.idx_start
        if self.idx_range >= data_length:
            self.idx_range = data_length
        if self.idx_range <= self._min_range:
            self.idx_range = self._min_range
        # 更新图表（注意因为多了一个参数idx_range，refresh_plot函数也有所改动）
        if scale_factor != 1:
            self._ax_price.clear()
            self._ax_volume.clear()
            self.refresh_plot()

    def close(self, event):
        # 将关闭标记置为True
        self._closed = True
