from gui.date_entry import *


class DateIntervalEntry(ttk.Frame):
    """输入日期区间的控件"""
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.fm_start_date = ttk.Frame(self)
        self.fm_start_date.pack(side=tk.LEFT, padx=5)
        self.fm_end_date = ttk.Frame(self)
        self.fm_end_date.pack(side=tk.LEFT, padx=5)
        self.lb_start = ttk.Label(self.fm_start_date, text='开始时间：')
        self.lb_start.grid(row=0, column=0, sticky=tk.W)
        self.de_start_time = DateEntry(self.fm_start_date)
        self.de_start_time.et_day.bind()
        self.de_start_time.grid(row=1, column=0)
        self.lb_end = ttk.Label(self.fm_end_date, text='结束时间：')
        self.lb_end.grid(row=0, column=0, sticky=tk.W)
        self.de_end_time = DateEntry(self.fm_end_date)
        self.de_end_time.et_year.bind()
        self.de_end_time.grid(row=1, column=0)

    def _cur_move(self, widget):
        """光标移动事件"""
        if widget == self.de_start_time.et_day:
            def func(e):
                if widget.index('insert') == widget.index('end'):
                    self.de_end_time.et_year.focus()
            return func
        elif widget == self.de_end_time.et_year:
            def func(e):
                if widget.index('insert') == 0:
                    self.de_start_time.et_day.focus()
                    self.de_start_time.et_day.icursor('end')
            return func

    def get(self):
        """取得日期区间"""
        stime = self.de_start_time.get()
        if stime is None:
            return
        etime = self.de_end_time.get()
        if etime is None:
            return
        if stime < etime:
            return stime, etime
        showerror('错误', '开始时间晚于结束时间！', parent=self)

    def set(self, stime, ctime):
        """设置日期区间"""
        self.de_start_time.set(stime)
        self.de_end_time.set(ctime)


if __name__ == '__main__':
    root = tk.Tk()
    de = DateIntervalEntry(root)
    de.pack()
    root.mainloop()
