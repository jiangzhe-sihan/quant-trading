import tkinter as tk


class SubWindow(tk.Toplevel):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.geometry('+{}+{}'.format(self.master.winfo_x() + 20, self.master.winfo_y() + 20))
        self._master_func = self.master.bind('<FocusIn>', self._flush_master, True)
        self.focus()
        self._func = self.bind('<FocusIn>', self._flush_self, True)

    @staticmethod
    def restack(ptr: tk.Misc):
        if ptr is None:
            return
        SubWindow.restack(ptr.master)
        ptr.lift()

    def _flush_master(self, event):
        if event.widget == self.master:
            self.restack(self.master)
            for v in self.master.children.values():
                if isinstance(v, SubWindow):
                    v.lift()
            if self.winfo_exists():
                self.focus()

    def _flush_self(self, event):
        if event.widget == self:
            self.restack(self)
            for v in self.master.children.values():
                if isinstance(v, SubWindow):
                    v.lift()

    def destroy(self) -> None:
        n = 0
        for v in self.master.children.values():
            if isinstance(v, SubWindow):
                n += 1
        if n == 1:
            self.master.unbind('<FocusIn>', self._master_func)
        self.master.focus()
        super().destroy()
