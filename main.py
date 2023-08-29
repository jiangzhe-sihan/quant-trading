import ctypes

from mttkinter.mtTkinter import Tk
from gui.scene_index import SceneIndex
from gui.scene import *
from gui.listbox_search import ListboxSearcher
from tools import init
# from multiprocessing import freeze_support


if __name__ == '__main__':
    # freeze_support()
    # 初始化
    init()
    # 主窗口
    root = Tk()
    # 告诉操作系统使用程序自身的dpi适配
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # 获取屏幕的缩放因子
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # 设置程序缩放
    root.tk.call('tk', 'scaling', ScaleFactor / 75)
    root.title('自研量化交易系统')
    root.iconbitmap(default='../favicon.ico')
    swidth = root.winfo_screenwidth() * ScaleFactor // 100
    sheight = root.winfo_screenheight() * ScaleFactor // 100
    width = 300
    height = 500
    root.geometry("%dx%d+%d+%d" % (width, height, (swidth - width) // 2, (sheight - height) // 2))
    ls = ListboxSearcher(root)
    ls.destroy()
    ss = SceneSwitcher(root)
    ss.set_home(SceneIndex)
    ss.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
