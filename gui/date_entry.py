import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
import datetime
from framework import Date


class DateEntry(ttk.Frame):
    """输入日期的控件"""
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.et_year = ttk.Entry(self)
        self.et_year.config(validate='all')
        self.et_year.config(validatecommand=(self.register(self._verify_year), '%P', '%S'))
        self.et_year['width'] = 4
        self.et_year.bind('<Key>', self._cur_move(self.et_year))
        self.et_year.bind('<Button-3>', self._right_click)
        self.et_year.grid(column=0, row=1)
        self.lb_joiner1 = ttk.Label(self)
        self.lb_joiner1['text'] = '-'
        self.lb_joiner1.grid(column=1, row=1)
        self.et_mon = ttk.Entry(self)
        self.et_mon.config(validate='all')
        self.et_mon.config(validatecommand=(self.register(self._verify_month), '%P', '%S'))
        self.et_mon['width'] = 2
        self.et_mon.bind('<Key>', self._cur_move(self.et_mon))
        self.et_mon.bind('<Button-3>', self._right_click)
        self.et_mon.grid(column=2, row=1)
        self.lb_joiner2 = ttk.Label(self)
        self.lb_joiner2['text'] = '-'
        self.lb_joiner2.grid(column=3, row=1)
        self.et_day = ttk.Entry(self)
        self.et_day.config(validate='all')
        self.et_day.config(validatecommand=(self.register(self._verify_start_day), '%P', '%S'))
        self.et_day['width'] = 2
        self.et_day.bind('<Key>', self._cur_move(self.et_day))
        self.et_day.bind('<Button-3>', self._right_click)
        self.et_day.grid(column=4, row=1)
        self._right_menu = tk.Menu(self, tearoff=0)
        self._right_menu.add_command(label='· 今天', command=self._goto_today)
        self._right_menu.add_command(label='<昨天', command=self._goto_yesterday)
        self._right_menu.add_command(label='>明天', command=self._goto_tomorrow)
        self._right_menu.add_command(label='<<上个月', command=self._goto_last_month)
        self._right_menu.add_command(label='>>下个月', command=self._goto_next_month)
        self._right_menu.add_command(label='<<<去年', command=self._goto_last_year)
        self._right_menu.add_command(label='>>>明年', command=self._goto_next_year)

    def _goto_today(self):
        today = datetime.datetime.today()
        self.set((today.year, today.month, today.day))

    def _goto_yesterday(self):
        today = Date(self.get_datetime())
        today.add_days(-1)
        self.set(today.date)

    def _goto_tomorrow(self):
        today = Date(self.get_datetime())
        today.add_days(1)
        self.set(today.date)

    def _goto_last_month(self):
        today = Date(self.get_datetime())
        today.add_month(-1)
        self.set(today.date)

    def _goto_next_month(self):
        today = Date(self.get_datetime())
        today.add_month(1)
        self.set(today.date)

    def _goto_last_year(self):
        today = Date(self.get_datetime())
        today.add_year(-1)
        self.set(today.date)

    def _goto_next_year(self):
        today = Date(self.get_datetime())
        today.add_year(1)
        self.set(today.date)

    def _right_click(self, event):
        self._right_menu.post(event.x_root, event.y_root)

    def _cur_move(self, widget):
        """光标移动事件"""
        if widget == self.et_year:
            def func(e):
                if widget.index('insert') == widget.index('end'):
                    if e.keysym == 'Right':
                        self.et_mon.focus()
            return func
        elif widget == self.et_mon:
            def func(e):
                if widget.index('insert') == widget.index('end'):
                    if e.keysym == 'Right':
                        self.et_day.focus()
                if widget.index('insert') == 0:
                    if e.keysym == 'Left':
                        self.et_year.focus()
                        self.et_year.icursor('end')
            return func
        elif widget == self.et_day:
            def func(e):
                if widget.index('insert') == 0:
                    if e.keysym == 'Left':
                        self.et_mon.focus()
                        self.et_mon.icursor('end')
            return func

    def _verify_year(self, content, key):
        """输入年份有效的验证"""
        if content == '':
            return True
        if key == ' ':
            self.et_mon.focus()
        if len(content) <= 4 and content.isdigit() and int(content) >= 1:
            return True
        return False

    def _verify_month(self, content, key):
        """输入月份有效的验证"""
        if content == '':
            return True
        if key == ' ':
            self.et_day.focus()
        if len(content) <= 2 and content.isdigit() and 1 <= int(content) <= 12:
            return True
        return False

    def _verify_start_day(self, content, key):
        """输入开始日期有效的验证"""
        if key == ' ':
            self.et_year.focus()
        if not (self.et_year.get() and self.et_mon.get()):
            return False
        if content == '':
            return True
        if len(content) <= 2 and content.isdigit():
            year = int(self.et_year.get())
            month = int(self.et_mon.get()) + 1
            if month > 12:
                if year != 9999:
                    year += 1
                    month = 1
                else:
                    month = 2
            temp = datetime.date(year, month, 1)
            temp -= datetime.timedelta(1)
            if 1 <= int(content) <= temp.day:
                return True
        return False

    def get(self):
        """取得日期"""
        if not (self.et_year.get() and self.et_mon.get() and self.et_day.get()):
            showerror('错误', '日期为空！', parent=self)
            return
        return int(self.et_year.get()), int(self.et_mon.get()), int(self.et_day.get())

    def get_datetime(self):
        """取得datetime类型的时间"""
        t = self.get()
        if t is not None:
            return datetime.datetime(*t)

    def set(self, date: tuple | datetime.datetime):
        """设置日期"""
        if type(date) == tuple:
            self.et_year.delete('0', 'end')
            self.et_year.insert('0', date[0])
            self.et_mon.delete('0', 'end')
            self.et_mon.insert('0', date[1])
            self.et_day.delete('0', 'end')
            self.et_day.insert('0', date[2])
        else:
            self.et_year.delete('0', 'end')
            self.et_year.insert('0', str(date.year))
            self.et_mon.delete('0', 'end')
            self.et_mon.insert('0', str(date.month))
            self.et_day.delete('0', 'end')
            self.et_day.insert('0', str(date.day))
        self.update()


if __name__ == '__main__':
    root = tk.Tk()
    de = DateEntry(root)
    de.pack()
    root.mainloop()
