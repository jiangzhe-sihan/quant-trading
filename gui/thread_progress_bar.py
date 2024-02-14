import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import *


class ThreadProgressBar(ttk.Progressbar):
    """线程进度条"""
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._td = None
        self._statu = tk.BooleanVar()
        self._idle_count = 0
        self._count = 0
        self._max = 0
        self._start_flag = False

    def is_running(self):
        return self._td is not None and self._td.is_alive()

    def _wait_thread_indeterminate(self):
        if self.is_running():
            self.update_idletasks()
            self.after(20, self._wait_thread_indeterminate)
        else:
            self.stop()
            self.config(mode='determinate')
            self._exit_thread()

    def _wait_thread_determinate(self):
        if self.is_running():
            progress, maximum = self._td.progress
            if maximum != self._max:
                self.config(maximum=maximum)
                self._max = maximum
            self._idle_count += 1
            if self._idle_count > 60 and progress == 0:
                if not self._start_flag:
                    self.config(mode='indeterminate')
                    self.start()
                    self._start_flag = True
            else:
                if self._start_flag:
                    self.stop()
                    self.config(mode='determinate')
                    self._start_flag = False
                self.step(progress - self._count)
                self._count = progress
            self.update_idletasks()
            self.after(20, self._wait_thread_determinate)
        else:
            self.stop()
            self._exit_thread()

    def _exit_thread(self):
        if self._td.code != 0:
            if self._td.msg is not None:
                msg = self._td.msg
            else:
                msg = str(self._td.exception)
            showerror(self._td.exception.__class__.__name__, msg, parent=self)
        self._td.join()
        self._td = None
        self._statu.set(not self._statu.get())
        self._idle_count = 0
        self.update()

    def load_thread(self, td):
        self._count = 0
        if not td.daemon:
            td.daemon = True
        self._td = td
        td.start()
        if hasattr(td, 'progress'):
            self._wait_thread_determinate()
        else:
            self.config(mode='indeterminate')
            self.start()
            self._wait_thread_indeterminate()
        self.waitvar(self._statu)
