from __future__ import annotations

import json
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo, askyesno, showerror
from tkinter.simpledialog import askfloat

import configure
from gui.pool_edit import PoolEditor
from gui.subwindow import SubWindow
from gui.vector_strategy_edit import VectorStrategyEditor
from template import get_strategy_template, get_strategy_path
from tools import load_config, save_config, get_stock_list


class Scene(tk.Frame):
    """所有场景的父类"""
    def __init__(self, name, master, **kw):
        super().__init__(master, **kw)
        self.config(bg=master.cget('bg'))
        self.name = name
        self.controller: tk.Misc | SceneSwitcher = master.master
        self.root = self.winfo_toplevel()


class SceneSwitcher(ttk.Frame):
    """管理gui场景的类"""
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        # 界面设计
        self.title = tk.StringVar()
        self.fm_top_title = tk.Frame(self, bg='#445469')
        self.fm_top_title.pack(side=tk.TOP, ipady=26, fill=tk.X)
        self.lb_top_hint = ttk.Label(self.fm_top_title, textvariable=self.title)
        self.lb_top_hint.config(font=('等线', 16), background='#445469', foreground='white')
        self.lb_top_hint.place(relx=.5, rely=.5, anchor=tk.CENTER)
        self.fm_mid_interface = tk.Frame(self)
        self.fm_mid_interface.pack(fill=tk.BOTH, expand=True)
        self.fm_bottom_navbar = tk.Frame(self, bg='#DDDFE2')
        self.fm_bottom_navbar.pack(side=tk.BOTTOM, ipady=25, fill=tk.X)
        self.bt_back = tk.Button(self.fm_bottom_navbar, text='<', relief='flat', overrelief='solid')
        self.bt_back.config(command=self.goto_back, activebackground='#CCCED0', bg='#DDDFE2', font=('times', 14))
        self.bt_back.place(relx=.25, rely=.5, anchor=tk.CENTER, relheight=.55, relwidth=.15)
        self.bt_home = tk.Button(self.fm_bottom_navbar, text='□', relief='flat', overrelief='solid', font=('meiryo',))
        self.bt_home.config(command=self.goto_home, activebackground='#CCCED0', bg='#DDDFE2')
        self.bt_home.place(relx=.5, rely=.5, anchor=tk.CENTER, relheight=.55, relwidth=.15)
        self.bt_setting = tk.Button(self.fm_bottom_navbar, text='≡', relief='flat', overrelief='solid')
        self.bt_setting.config(command=self.goto_setting, activebackground='#CCCED0', bg='#DDDFE2', font=('times', 20))
        self.bt_setting.place(relx=.75, rely=.5, anchor=tk.CENTER, relheight=.55, relwidth=.15)
        self.bind('<Destroy>', self._close)
        # 实例属性
        self._home = None  # 主页
        self._li_scene: list[type] = []  # 场景栈
        self._di_scene: dict[type, Scene] = {SceneSetting: SceneSetting(self.fm_mid_interface)}  # 场景表
        self._current = None  # 当前场景
        self.setting: Scene | SceneSetting = self._di_scene[SceneSetting]  # 设置项
        self._closed = False  # 关闭标记

    def _close(self, event):
        self._closed = True

    def load_scene(self, scene: type):
        """加载场景"""
        if self._current is None:
            self._li_scene.append(self._home)
        else:
            if scene == self._current:
                return
            self._li_scene.append(type(self._current))
            self._current.place_forget()
        if scene not in self._di_scene:
            self._di_scene[scene] = scene(self.fm_mid_interface)
        self._current = self._di_scene[scene]
        self._current.place(anchor=tk.N, relx=.5, rely=.05)
        self.title.set(self._current.name)

    def set_home(self, scene: type):
        """设置主页"""
        self._li_scene.clear()
        self._home = scene
        self.load_scene(scene)

    def goto_back(self):
        """返回上一界面"""
        if len(self._li_scene) > 1:
            scene = self._li_scene.pop(-1)
            self.load_scene(scene)
            self._li_scene.pop(-1)

    def goto_home(self):
        """返回主页"""
        self.load_scene(self._home)
        self._li_scene = self._li_scene[:1]

    def goto_setting(self):
        """转到设置界面"""
        self.load_scene(SceneSetting)
        self.setting.update_config()

    def disable(self):
        """禁用按钮功能"""
        if self._closed:
            return
        self.bt_back.config(state='disabled')
        self.bt_home.config(state='disabled')
        self.bt_setting.config(state='disabled')

    def enable(self):
        """启用按钮功能"""
        if self._closed:
            return
        self.bt_back.config(state='normal')
        self.bt_home.config(state='normal')
        self.bt_setting.config(state='normal')


class SceneSetting(Scene):
    """设置场景"""
    _instance: SceneSetting = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> SceneSetting:
        return cls.__new__(cls)

    def __init__(self, master, **kw):
        super().__init__('设置', master, **kw)
        # 界面设计
        bg = master.cget('bg')
        self.fm_pool = ttk.Frame(self)
        self.fm_pool.pack()
        self.lb_pool = ttk.Label(self.fm_pool, text='股票池：', cursor='hand2')
        self.lb_pool.bind('<Enter>', self._lb_pool_enter)
        self.lb_pool.bind('<Button-1>', self._lb_pool_click)
        self.lb_pool.bind('<Leave>', self._lb_pool_leave)
        self.lb_pool.grid(row=0, column=0)
        self.str_pool = tk.StringVar()
        self.cb_pool = ttk.Combobox(self.fm_pool, textvariable=self.str_pool, width=16)
        self.cb_pool.config(validate='key')
        self.cb_pool.config(validatecommand=(self.register(lambda: False)))
        self.cb_pool.config(invalidcommand=(self.register(self._pool_search), '%S'))
        self.cb_pool.grid(row=0, column=1)
        self.bt_pool_help = tk.Button(self.fm_pool, text='?', relief='flat', command=self._show_pool_help)
        self.bt_pool_help.config(overrelief='ridge', bg=bg)
        self.bt_pool_help.grid(row=0, column=2)
        self.fm_channel = ttk.Frame(self)
        self.fm_channel.pack()
        self.lb_channel = ttk.Label(self.fm_channel, text='数据频道：', cursor='hand2')
        self.lb_channel.bind('<Enter>', self._lb_channel_enter)
        self.lb_channel.bind('<Button-1>', self._lb_channel_click)
        self.lb_channel.bind('<Leave>', self._lb_channel_leave)
        self.lb_channel.grid(row=0, column=0)
        self.str_channel = tk.StringVar()
        self.cb_channel = ttk.Combobox(self.fm_channel, textvariable=self.str_channel, width=14)
        self.cb_channel.config(validate='key')
        self.cb_channel.config(validatecommand=(self.register(lambda: False)))
        self.cb_channel.config(invalidcommand=(self.register(self._channel_search), '%S'))
        self.cb_channel.grid(row=0, column=1)
        self.bt_channel_help = tk.Button(self.fm_channel, text='?', relief='flat')
        self.bt_channel_help.config(command=self._show_channel_help, overrelief='ridge', bg=bg)
        self.bt_channel_help.grid(row=0, column=2)
        self.fm_strategy = ttk.Frame(self)
        self.fm_strategy.pack()
        self.lb_strategies = ttk.Label(self.fm_strategy, text='策略：', cursor='hand2')
        self.lb_strategies.bind('<Enter>', self._lb_strategies_enter)
        self.lb_strategies.bind('<Button-1>', self._lb_strategies_click)
        self.lb_strategies.bind('<Leave>', self._lb_strategies_leave)
        self.lb_strategies.grid(row=0, column=0, sticky=tk.W)
        self.lsb_strategies = tk.Listbox(self.fm_strategy, width=25)
        self.lsb_strategies.bind('<Button-3>', self._right_click)
        self.lsb_strategies.grid(row=1, column=0, columnspan=3)
        self.str_strategy = tk.StringVar()
        self.cb_strategy = ttk.Combobox(self.fm_strategy, textvariable=self.str_strategy, width=16)
        self.cb_strategy.config(validate='key')
        self.cb_strategy.config(validatecommand=(self.register(lambda: False)))
        self.cb_strategy.config(invalidcommand=(self.register(self._strategy_search), '%S'))
        self.cb_strategy.grid(row=2, column=0)
        self.bt_add_strategy = ttk.Button(self.fm_strategy, text='+', width=2)
        self.bt_add_strategy.config(command=self._add_strategy)
        self.bt_add_strategy.grid(row=2, column=1)
        self.bt_strategy_help = tk.Button(self.fm_strategy, text='?', relief='flat')
        self.bt_strategy_help.config(command=self._show_strategy_help, overrelief='ridge', bg=bg)
        self.bt_strategy_help.grid(row=2, column=2)
        self.bt_confirm = ttk.Button(self, text='确认', command=self._confirm)
        self.bt_confirm.pack()
        # 实例属性
        self.channel_loader = configure.ChannelLoader()
        self.pool_loader = configure.StockPoolLoader()
        self.strategy_loader = None
        self.strategy_mode = load_config().get('strategy_mode', 'code')
        self._swnd_pool = {}
        self._swnd_channel = {}
        self._swnd_strategy = {}
        # 初始化
        self.update_config()

    def _lb_pool_enter(self, event):
        self.lb_pool.config(foreground='blue', underline=True)

    def _lb_pool_click(self, event):
        mb = tk.Menu(self, tearoff=0)
        mb.add_command(label='新建股票池', command=self._new_pool)
        mb.add_command(label='删除股票池', command=self._del_pool)
        mb.add_separator()
        mb.add_command(label='在资源管理器中打开', command=lambda: os.system('start ' + '..\\pools\\'))
        mb.post(event.x_root, event.y_root)

    def _new_pool(self):
        if self._swnd_pool.get('*new_pool', None) is not None:
            self._swnd_pool['*new_pool'].focus()
            return
        swnd = SubWindow(self.winfo_toplevel())
        swnd.title('新建股票池')
        fm_entry = tk.Frame(swnd)
        fm_entry.pack(padx=40)
        fm_name = tk.Frame(fm_entry)
        fm_name.pack(pady=5, fill=tk.X)
        lb_name = tk.Label(fm_name, text='池名称')
        lb_name.pack(side=tk.LEFT)
        et_name = tk.Entry(fm_name)
        et_name.pack(side=tk.RIGHT)
        fm_extra = tk.Frame(fm_entry)
        fm_extra.pack(pady=5, fill=tk.X)
        lb_extra = tk.Label(fm_extra, text='附加选项')
        lb_extra.pack(side=tk.LEFT)
        option = tk.StringVar()
        mub_extra = ttk.OptionMenu(fm_extra, option, '无', '无', '导入沪深300', '导入中证500', '导入上证50')
        mub_extra.config(width=12)
        mub_extra.pack(side=tk.RIGHT)

        def confirm():
            if et_name.get().strip() == '':
                showinfo('失败', '请输入池名称', parent=swnd)
                return
            name = et_name.get().strip()
            try:
                match option.get():
                    case '导入沪深300':
                        li = get_stock_list('fs=b:BK0500')['data']['diff']
                    case '导入中证500':
                        li = get_stock_list('fs=b:BK0701+f:!2')['data']['diff']
                    case '导入上证50':
                        li = get_stock_list('fs=b:BK0611')['data']['diff']
                    case default:
                        li = []
            except Exception as e:
                showinfo('失败', str(e))
                return
            pwd = '../pools/'
            if os.path.exists(pwd + name + '.json'):
                showinfo('失败', '股票池已存在', parent=swnd)
                return
            res = []
            for i in li:
                res.append(f'{i["f13"]}.{i["f12"]}')
            fp = open(pwd + name + '.json', 'w+')
            json.dump(res, fp)
            fp.close()
            showinfo('成功', '股票池已创建', parent=swnd)
            self.update_config()
            swnd.destroy()
        bt_confirm = ttk.Button(swnd, text='创建', command=confirm)
        bt_confirm.pack(pady=10)
        self._swnd_pool['*new_pool'] = swnd
        self.wait_window(swnd)
        self._swnd_pool.pop('*new_pool')

    def _del_pool(self):
        name = self.str_pool.get()
        if name.strip() == '':
            showerror('错误', '没有选中任何股票池', parent=self.winfo_toplevel())
            return
        act = askyesno('删除', f'你确定删除股票池{name}？', parent=self.winfo_toplevel())
        if not act:
            return
        pwd = '../pools/'
        os.unlink(pwd + name + '.json')
        showinfo('成功', f'已删除股票池{name}', parent=self.winfo_toplevel())
        self.update_config()

    def _lb_pool_leave(self, event):
        self.lb_pool.config(foreground='black', underline=False)

    def _lb_channel_enter(self, event):
        self.lb_channel.config(foreground='blue', underline=True)

    def _lb_channel_click(self, event):
        mb = tk.Menu(self, tearoff=0)
        mb.add_command(label='在资源管理器中打开', command=lambda: os.system('start ' + '..\\channels\\'))
        mb.post(event.x_root, event.y_root)

    def _lb_channel_leave(self, event):
        self.lb_channel.config(foreground='black', underline=False)

    def _lb_strategies_enter(self, event):
        self.lb_strategies.config(foreground='blue', underline=True)

    def _lb_strategies_click(self, event):
        mb = tk.Menu(self, tearoff=0)
        mb.add_command(label='新建策略', command=self._new_strategy)
        mb.add_command(label='删除策略', command=self._del_strategy)
        mb.add_separator()
        mb.add_command(label='在资源管理器中打开', command=lambda: os.system('start ' + '..\\strategies\\'))
        mb.add_separator()
        mb_mode = tk.Menu(self, tearoff=0)
        mb.add_cascade(label='修改策略模式', menu=mb_mode)
        mb_mode.add_command(label='代码模式', command=lambda: self._switch_mode('code'))
        mb_mode.add_command(label='向量模式', command=lambda: self._switch_mode('vector'))
        mb.post(event.x_root, event.y_root)

    def _new_strategy(self):
        if self._swnd_strategy.get('*new_strategy', None) is not None:
            self._swnd_strategy['*new_strategy'].focus()
            return
        swnd = SubWindow(self.winfo_toplevel())
        swnd.title('新建策略')
        fm_entry = tk.Frame(swnd)
        fm_entry.pack(padx=5)
        fm_name = tk.Frame(fm_entry)
        fm_name.pack(pady=5, fill=tk.X)
        lb_name = tk.Label(fm_name, text='策略名称')
        lb_name.pack(side=tk.LEFT)
        et_name = tk.Entry(fm_name)
        et_name.pack(side=tk.RIGHT)
        fm_desc = tk.Frame(fm_entry)
        fm_desc.pack(pady=5, fill=tk.X)
        lb_desc = tk.Label(fm_desc, text='策略描述（可选）')
        lb_desc.pack(side=tk.LEFT)
        et_desc = tk.Entry(fm_desc)
        et_desc.pack(side=tk.RIGHT)
        fm_simi = tk.Frame(fm_entry)
        fm_simi.pack(pady=5, fill=tk.X)
        lb_simi = tk.Label(fm_simi, text='默认相似度')
        lb_simi.pack(side=tk.LEFT)
        et_simi = tk.Entry(fm_simi)
        et_simi.insert(0, '0.98')
        et_simi.pack(side=tk.RIGHT)

        def confirm():
            if et_name.get().strip() == '':
                showinfo('失败', '请输入策略名称', parent=swnd)
                return
            name = et_name.get().strip()
            desc = et_desc.get().strip()
            pwd = get_strategy_path()
            match self.strategy_mode:
                case 'vector':
                    ex_name = '.vec'
                case default:
                    ex_name = '.py'
            if os.path.exists(pwd + name + ex_name):
                showerror('失败', '策略已存在', parent=swnd)
                return
            match self.strategy_mode:
                case 'vector':
                    try:
                        simi = float(et_simi.get())
                    except ValueError:
                        showerror('失败', '相似度必须是数字', parent=swnd)
                        return
                    if simi < 0 or simi > 1:
                        showerror('失败', '相似度在0~1之间', parent=swnd)
                        return
                    fm_entry.forget()
                    bt_confirm.forget()
                    editor = VectorStrategyEditor(swnd, path=pwd + name + ex_name, name=name, desc=desc, simi=simi)
                    editor.pack()
                case default:
                    model = get_strategy_template(name, desc)
                    fp = open(pwd + name + ex_name, 'w+')
                    fp.write(model)
                    fp.close()
                    showinfo('成功', '策略已创建', parent=swnd)
                    self.update_config()
                    swnd.destroy()
        bt_confirm = ttk.Button(swnd, text='创建', command=confirm)
        bt_confirm.pack(pady=10)
        self._swnd_strategy['*new_strategy'] = swnd
        self.wait_window(swnd)
        self._swnd_strategy.pop('*new_strategy')
        self.update_config()

    def _del_strategy(self):
        name = self.str_strategy.get()
        if name.strip() == '':
            showerror('错误', '没有选中任何策略', parent=self.winfo_toplevel())
            return
        act = askyesno('删除', f'你确定删除策略{name}？', parent=self.winfo_toplevel())
        if not act:
            return
        pwd = get_strategy_path()
        match self.strategy_mode:
            case 'vector':
                ex_name = '.vec'
                ved = pwd + name + '.ved'
                if os.path.exists(ved):
                    os.unlink(ved)
            case default:
                ex_name = '.py'
        os.unlink(pwd + name + ex_name)
        showinfo('成功', f'已删除策略{name}', parent=self.winfo_toplevel())
        self.update_config()

    def _lb_strategies_leave(self, event):
        self.lb_strategies.config(foreground='black', underline=False)

    def _switch_mode(self, mode: str):
        self.strategy_mode = mode
        self.update_config()

    def update_config(self):
        cfg = load_config()
        self.str_pool.set(cfg['pool'])
        self.cb_pool.config(values=self.pool_loader.get_pools_list())
        self.str_channel.set(cfg['channel'])
        self.cb_channel.config(values=self.channel_loader.get_channel_list())
        match self.strategy_mode:
            case 'code':
                self.strategy_loader = configure.StrategyLoader()
                self.lb_strategies.config(text='策略（代码模式）：')
            case 'vector':
                self.strategy_loader = configure.VectorStrategyLoader()
                self.lb_strategies.config(text='策略（向量模式）：')
        li_stg = self.strategy_loader.get_strategy_list()
        self.str_strategy.set(li_stg[0] if li_stg else '')
        self.cb_strategy.config(values=self.strategy_loader.get_strategy_list())
        self.lsb_strategies.delete('0', 'end')
        for i in cfg['strategy_' + self.strategy_mode]:
            self.lsb_strategies.insert('end', i)

    def _pool_search(self, content):
        for i in self.cb_pool['values']:
            if i.startswith(content):
                self.cb_pool.set(i)
                return
        self.cb_pool.set(self.cb_pool['values'][0])

    def _channel_search(self, content):
        for i in self.cb_channel['values']:
            if i.startswith(content):
                self.cb_channel.set(i)
                return
        self.cb_channel.set(self.cb_channel['values'][0])

    def _strategy_search(self, content):
        for i in self.cb_strategy['values']:
            if i.startswith(content):
                self.cb_strategy.set(i)
                return
        self.cb_strategy.set(self.cb_strategy['values'][0])

    def _show_pool_help(self):
        self.bell()
        pool_name = self.cb_pool.get()
        if pool_name in self._swnd_pool:
            self._swnd_pool[pool_name].focus()
            return
        pool = '../pools/' + pool_name + '.json'
        swnd = SubWindow(self.root)
        swnd.title(pool_name)
        swnd.geometry('300x360')
        pe = PoolEditor(swnd)
        pe.pack()
        pe.load(pool)
        self._swnd_pool[pool_name] = swnd
        self.wait_window(swnd)
        self._swnd_pool.pop(pool_name)

    def _show_channel_help(self):
        self.bell()
        channel_name = self.channel
        if channel_name in self._swnd_pool:
            self._swnd_channel[channel_name].focus()
            return
        chn = self.channel_loader.get_channel(channel_name)
        swnd = SubWindow(self.root)
        swnd.title(channel_name)
        lb_name = ttk.Label(swnd, text=chn.name)
        lb_name.pack()
        lb_des = ttk.Label(swnd, text=chn.description)
        lb_des.pack()
        lb_hint = ttk.Label(swnd, text='-*不能获取数据可能是因为没有设置在正确的频道*-', foreground='red')
        lb_hint.pack(pady=10)
        self._swnd_channel[channel_name] = swnd
        self.wait_window(swnd)
        self._swnd_channel.pop(channel_name)

    def _show_strategy_help(self):
        self.bell()
        strategy_name = self.str_strategy.get()
        if strategy_name in self._swnd_strategy:
            self._swnd_strategy[strategy_name].focus()
            return
        chn = self.strategy_loader.get_strategy(strategy_name)
        swnd = SubWindow(self.root)
        swnd.title(strategy_name)
        lb_name = ttk.Label(swnd, text=chn.name)
        lb_name.pack()
        lb_des = ttk.Label(swnd, text=chn.description)
        lb_des.pack()
        self._swnd_strategy[strategy_name] = swnd
        self.wait_window(swnd)
        self._swnd_strategy.pop(strategy_name)

    def _add_strategy(self):
        li = self.lsb_strategies.get(0, 'end')
        if not self.str_strategy.get() or self.str_strategy.get() in li:
            return
        self.lsb_strategies.insert('end', self.str_strategy.get())

    def _delete_strategy(self):
        selected = self.lsb_strategies.curselection()
        for i in selected[::-1]:
            self.lsb_strategies.delete(i)

    def _right_click(self, event):
        if not self.lsb_strategies.curselection():
            return
        if self.lsb_strategies.curselection()[0] != self.lsb_strategies.nearest(event.y):
            return
        mu = tk.Menu(self.lsb_strategies, tearoff=0)
        mu.add_command(label='删除', command=self._delete_strategy)
        if self.strategy_mode == 'vector':
            mu.add_separator()
            mu.add_command(label='修改相似度', command=self._modify_simi)
        mu.post(event.x_root, event.y_root)

    def _modify_simi(self):
        selected = self.lsb_strategies.curselection()
        name = self.lsb_strategies.get(selected[0])
        sc = self.strategy_loader.get_strategy(name)
        simi = askfloat("修改相似度", "请输入相似度",
                        initialvalue=sc.simi, maxvalue=1.0, minvalue=0.0, parent=self.winfo_toplevel())
        if simi is None:
            return
        self.strategy_loader.update(name, simi)
        showinfo("完成", "修改相似度成功", parent=self.winfo_toplevel())

    @property
    def pool(self):
        cfg = load_config()
        return cfg['pool']

    @property
    def channel(self):
        cfg = load_config()
        return cfg['channel']

    @property
    def strategy(self):
        return list(self.lsb_strategies.get(0, 'end'))

    def _confirm(self):
        cfg = {
            'pool': self.str_pool.get(),
            'channel': self.str_channel.get(),
            'strategy_mode': self.strategy_mode,
            'strategy_' + self.strategy_mode: self.strategy
        }
        cfg_ = load_config()
        for k in cfg.keys():
            cfg_.pop(k)
        cfg.update(cfg_)
        save_config(cfg)
        showinfo('完成', '配置写入成功！', parent=self.root)
