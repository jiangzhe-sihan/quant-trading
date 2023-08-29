import tkinter as tk


class StdGuiIO(tk.Text):
    """基于tkinter gui的标准输入输出流"""
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.config(spacing1=12)
        self.config(wrap='word')
        self.config(state='disabled')
        self.bind('<Button-3>', self._right_click)

    def write(self, string):
        """写入字符串"""
        self.config(state='normal')
        self.insert('end', string)
        self.config(state='disabled')
        self.yview_moveto(1.0)
        self.update()

    def blit(self, index1, index2, string):
        """更新区块"""
        self.config(state='normal')
        self.delete(index1, index2)
        self.insert(index1, string)
        self.config(state='disabled')
        self.update()

    def clear(self):
        """清空内容"""
        self.config(state='normal')
        self.delete('0.0', 'end')
        self.config(state='disabled')
        self.update()

    def _right_click(self, event):
        try:
            content = self.selection_get()
        except tk.TclError:
            return

        def func():
            self.clipboard_clear()
            self.clipboard_append(content)
        mb = tk.Menu(self, tearoff=0)
        mb.add_command(label='复制', command=func)
        mb.post(event.x_root, event.y_root)
