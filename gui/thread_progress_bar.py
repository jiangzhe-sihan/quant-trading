import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import *


class ThreadProgressBar(ttk.Progressbar):
    """线程进度条"""
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._progress = tk.IntVar()
        self.config(variable=self._progress)
        self._td = None
        self._statu = tk.BooleanVar()
        self._idle_count = 0

    def is_running(self):
        return self._td is not None and self._td.is_alive()

    def _wait_thread_indeterminate(self):
        if self.is_running():
            self.update_idletasks()
            self.after(10, self._wait_thread_indeterminate)
        else:
            self.stop()
            self.config(mode='determinate')
            self._exit_thread()

    def _wait_thread_determinate(self):
        if self.is_running():
            length = self.cget('maximum')
            progress = int(length * self._td.progress) if self._td.progress < 1 else length
            self._idle_count += 1
            if self._idle_count > 60 and progress == 0:
                self.config(mode='indeterminate')
                self.start()
            else:
                self.stop()
                self.config(mode='determinate')
                self._progress.set(progress)
            self.update_idletasks()
            self.after(10, self._wait_thread_determinate)
        else:
            self._progress.set(0)
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
