import tkinter as tk
import tkinter.ttk as ttk
import json
from tkinter.messagebox import askyesno

import requests

from general_thread import ProgressThread, MultiThreadLoader
from gui.listbox_search import ListboxSearcher
import tools
from gui.thread_progress_bar import ThreadProgressBar


class DynamicEntry(ttk.Entry):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._his = tk.StringVar()
        self._mod_semaphore = tk.BooleanVar()
        self._mod_flag = False
        self._start_monitor = False
        self._key = None
        self.start_monitor()

    def get_key(self):
        return self._key

    def set_key(self, value: str):
        self._key = value

    def start_monitor(self):
        if self._start_monitor:
            return
        self.get_modified()
        self._start_monitor = True
        self._monitor()

    def stop_monitor(self):
        self._start_monitor = False

    def _monitor(self):
        if not self._start_monitor:
            return
        if self.get_modified():
            self.after(300, self._confirm_modified)
            self.wait_variable(self._mod_semaphore)
            if not self._mod_flag:
                self.event_generate('<<Modified>>')
                self._key = None
        self.after(500, self._monitor)

    def get_modified(self):
        s = self.get()
        if s == self._his.get():
            self._mod_flag = False
        else:
            self._mod_flag = True
        self._his.set(s)
        return self._mod_flag

    def _confirm_modified(self):
        self.get_modified()
        self._mod_semaphore.set(not self._mod_semaphore.get())

    def fill(self, string: str):
        self.delete('0', 'end')
        self.insert('insert', string)


class PoolEditor(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        # 界面设置
        self._lb_hint = tk.Label(self, text='该股票池包含如下标的：')
        self._lb_hint.pack(anchor=tk.W)
        self._fm_lsb = tk.Frame(self)
        self._fm_lsb.pack()
        self._lsb = tk.Listbox(self._fm_lsb, width=30)
        self._lsb.pack(side=tk.LEFT)
        self._sb = ttk.Scrollbar(self._fm_lsb, command=self._lsb.yview)
        self._sb.pack(side=tk.LEFT, fill=tk.Y)
        self._lsb.config(yscrollcommand=self._sb.set)
        self._lsb.bind('<Button-3>', self._right_click)
        self._searcher = ListboxSearcher(self)
        self._searcher.set_size(24)
        self._searcher.pack()
        self._searcher.set_listbox([self._lsb])
        et = self._searcher.get_entry()
        et.bind('<FocusIn>', lambda x: self._lb_local_search.place_forget())
        et.bind(
            '<FocusOut>',
            lambda x: self._lb_local_search.place(relx=.01, rely=.1, relheight=.8) if not et.get() else None)
        self._lb_local_search = tk.Label(et, text='本地搜索')
        self._lb_local_search.config(bg='white', fg='grey')
        self._lb_local_search.bind('<Button-1>', lambda x: et.focus())
        self._lb_local_search.place(relx=.01, rely=.1, relheight=.8)
        self._fm_new_symbol = tk.Frame(self)
        self._fm_new_symbol.pack()
        self._web_searcher = DynamicEntry(self._fm_new_symbol, width=30)
        self._web_searcher.bind('<<Modified>>', lambda x: self._search(x.widget.get()))
        self._web_searcher.bind('<Key-Return>', lambda x: self._search(x.widget.get()))
        self._web_searcher.bind('<FocusIn>', lambda x: self._lb_new.place_forget())
        self._web_searcher.bind(
            '<FocusOut>',
            lambda x: self._lb_new.place(relx=.01, rely=.1, relheight=.8) if not self._web_searcher.get() else None)
        self._web_searcher.pack(side=tk.LEFT)
        self._lb_new = tk.Label(self._web_searcher, text='新标的', bg='white', fg='grey')
        self._lb_new.bind('<Button-1>', lambda x: self._web_searcher.focus())
        self._lb_new.place(relx=.01, rely=.1, relheight=.8)
        self._bt_new = ttk.Button(self._fm_new_symbol, text='+', width=2, command=self._add_symbol)
        self._bt_new.pack(side=tk.LEFT)
        self._separator = ttk.Separator(self, orient='horizontal')
        self._separator.pack(pady=15, fill=tk.X)
        self._fm_btn = tk.Frame(self)
        self._fm_btn.pack()
        self._bt_save = ttk.Button(self._fm_btn, text='保存', command=self._save_edit)
        self._bt_save.pack()
        self.progress_bar = ThreadProgressBar(self)
        # 实例属性
        self._li_pool: list[str] = []
        self._session = requests.Session()
        self._quotation = None
        self._src = None
        self._src_type = None

    def insert(self, *elem):
        for e in elem:
            if e not in self._li_pool:
                self._li_pool.append(e)
            self.update_idletasks()
        self.update_idletasks()

    def load(self, src: str | tuple | list | set):
        if type(src) == str:
            if '.json' in src:
                self._load_from_json(src)
            else:
                raise TypeError('不支持的格式！')
        else:
            self._src = src
            self._src_type = 'datastructure'
            self.insert(*src)
        self.after_idle(self._flush)

    def _load_from_json(self, src: str):
        self._src = src
        self._src_type = 'json'
        with open(src) as fp:
            data = json.load(fp)
        self.insert(*data)

    def get_lsb(self):
        return self._lsb

    def _add_symbol(self):
        if not self._web_searcher.get().strip():
            return
        if self._web_searcher.get_key() is None:
            act = askyesno(
                '注意',
                f'标的"{self._web_searcher.get()}"未经过联网验证。\n仍然添加？',
                parent=self.winfo_toplevel()
            )
            if not act:
                return
            self._insert_symbol()
        else:
            self._insert_symbol(confirmed=True)

    def _insert_symbol(self, confirmed=False):
        if confirmed:
            symbol = self._web_searcher.get_key()
        else:
            symbol = self._web_searcher.get()
        if symbol in self._li_pool:
            index = self._li_pool.index(symbol)
            self._lsb.select_clear(0, 'end')
            self._lsb.select_set(index)
            self._lsb.see(index)
            return
        self._li_pool.append(symbol)
        self._lsb.insert('end', self._web_searcher.get())
        self._lsb.select_clear(0, 'end')
        self._lsb.select_set('end')
        self._lsb.see('end')

    def _delete_symbol(self, index):
        self._lsb.delete(index)
        self._li_pool.pop(index)

    def _save_edit(self):
        match self._src_type:
            case 'json':
                with open(self._src) as fp:
                    src = json.load(fp)
                if self._li_pool == src:
                    tk.messagebox.showinfo('完成', '没有任何更改！', parent=self.winfo_toplevel())
                    return
                with open(self._src, 'w+') as fp:
                    json.dump(self._li_pool, fp)
                tk.messagebox.showinfo('完成', '股票池更新成功！', parent=self.winfo_toplevel())
            case 'datastructure':
                if self._li_pool == self._src:
                    tk.messagebox.showinfo('完成', '没有任何更改！', parent=self.winfo_toplevel())
                    return
                self._src.clear()
                if type(self._src) == list:
                    self._src.extend(self._li_pool)
                elif type(self._src) == set:
                    self._src.update(self._li_pool)
                else:
                    raise TypeError('不支持修改！')
                tk.messagebox.showinfo('完成', '股票池更新成功！', parent=self.winfo_toplevel())

    def _right_click(self, event):
        cur = self._lsb.curselection()
        if not cur:
            return
        if cur[0] != self._lsb.nearest(event.y):
            return
        mu = tk.Menu(self, tearoff=0)
        mu.add_command(label='删除', command=lambda: self._delete_symbol(cur[0]))
        mu.post(event.x_root, event.y_root)

    def _search(self, code, session: requests.Session = None):
        if self._quotation is not None:
            self._quotation.destroy()
        if not code.strip():
            return
        if session is None:
            session = self._session
        try:
            resp = session.get(
                'https://searchadapter.eastmoney.com/api/suggest/get',
                headers={
                    'User-Agent': tools.get_user_agent(),
                    'Referer': 'https://quote.eastmoney.com/',
                    'Host': 'searchadapter.eastmoney.com'
                },
                params={'input': code, 'type': 14, 'count': 5},
                timeout=3
            )
            res = resp.json()
            self._quotation = tk.Menu(self._web_searcher, tearoff=0)
            for i in res['QuotationCodeTable']['Data']:
                quote_id = i["QuoteID"]
                name = i["Name"]

                def command(a=quote_id, b=name):
                    self._web_searcher.stop_monitor()
                    self._web_searcher.fill(f'[{a}]{b}')
                    self._web_searcher.set_key(a)
                    self._web_searcher.start_monitor()

                self._quotation.add_command(label=f'[{quote_id}]{name}', command=command)
        except TimeoutError:
            self._quotation = tk.Menu(self._web_searcher, tearoff=0)
            self._quotation.add_command(label='网络连接失败', foreground='red')
        except:
            self._quotation = tk.Menu(self._web_searcher, tearoff=0)
            self._quotation.add_command(label='没有联网提示', foreground='red')
        finally:
            x = self._web_searcher.winfo_rootx()
            y = self._web_searcher.winfo_rooty() + self._web_searcher.winfo_reqheight()
            self._quotation.post(x, y)

    def fresh_item(self, index, value):
        self._lsb.delete(index)
        self._lsb.insert(index, value)

    def _flush(self):
        self._lsb.config(cursor='watch')
        self._lsb.insert('end', *self._li_pool)
        tasks = []
        session = tools.get_requests_session()
        ua = tools.get_user_agent()
        for i in range(len(self._li_pool)):
            item = self._li_pool[i]
            if '.' in item:
                sp = item.split('.')
                code = sp[1]
                match sp[0]:
                    case 'sh':
                        full_code = f'1.{code}'
                    case 'sz':
                        full_code = f'0.{code}'
                    case default:
                        full_code = item
            else:
                code = item
                full_code = item

            def search(index, en, co, callback):
                return index, en, co, tools.connect(
                    'https://searchadapter.eastmoney.com/api/suggest/get', session,
                    headers={
                        'User-Agent': ua,
                        'Referer': 'https://quote.eastmoney.com/',
                        'Host': 'searchadapter.eastmoney.com'
                    },
                    params={'input': en, 'type': 14, 'count': 5}
                )
            tasks.append(ProgressThread(search, (i, code, full_code)))
        sem = 6
        for i in range(0, len(tasks), sem):
            tds = tasks[i:i+sem]
            td = MultiThreadLoader(tds)
            self.progress_bar.load_thread(td)
            for index, en, co, res in td.res:
                resp = json.loads(res)
                count = len(resp['QuotationCodeTable']['Data'])
                if count == 0:
                    self.fresh_item(index, f'[{co}] [-退-]')
                    self.get_lsb().itemconfig(index, fg='red')
                    self.update()
                    continue
                data = resp['QuotationCodeTable']['Data']
                name = None
                for d in data:
                    if d['QuoteID'] == co:
                        name = d
                        break
                if name is None:
                    for d in data:
                        if d['UnifiedCode'] == en:
                            name = d
                            break
                if name is None:
                    self.fresh_item(index, f'[{co}] [-退-]')
                    self.get_lsb().itemconfig(index, fg='red')
                    self.update()
                self.fresh_item(index, f'[{name["QuoteID"]}]{name["Name"]}')
                self.update()
        session.close()
        self._lsb.config(cursor='arrow')
