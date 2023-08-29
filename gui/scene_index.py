import tkinter.ttk as ttk
from gui.scene import Scene
from gui.scene_backtest import SceneBacktest
from gui.scene_recommend import SceneRecommend
# from debug import main


class SceneIndex(Scene):
    def __init__(self, master, **kw):
        super().__init__('功能选择', master, **kw)
        self.bt_backtest = ttk.Button(self, text='策略回测')
        self.bt_backtest.config(command=self._backtest)
        self.bt_backtest.pack(pady=5)
        self.bt_recommend = ttk.Button(self, text='今日发牌')
        self.bt_recommend.config(command=self._recommend)
        self.bt_recommend.pack(pady=5)
        # self.bt_recommend = ttk.Button(self, text='测试按钮')
        # self.bt_recommend.config(command=self._test)
        # self.bt_recommend.pack(pady=5)

    def _backtest(self):
        self.controller.load_scene(SceneBacktest)

    def _recommend(self):
        self.controller.load_scene(SceneRecommend)

    def _test(self):
        pass
