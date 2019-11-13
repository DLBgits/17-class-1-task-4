# -*- coding: utf-8 -*-
# @Date    : 2018-10-30
# @Author  : Don't know
# @Editor  : 黄炫智 耿晟昶

import tkinter as tk
import tkinter.ttk as ttk

#查找与替换
class FindWindow(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)

        self.master = master

        self.geometry('350x100')
        self.title('Find and Replace')
        self.transient(self.master)
        self.configure(bg=self.master.master.background)

        self.text_to_find = tk.StringVar()
        self.text_to_replace_with = tk.StringVar()

        top_frame = tk.Frame(self, bg=self.master.master.background)
        middle_frame = tk.Frame(self, bg=self.master.master.background)
        bottom_frame = tk.Frame(self, bg=self.master.master.background)

        find_entry_label = ttk.Label(top_frame, text="Find: ", style="editor.TLabel")
        self.find_entry = ttk.Entry(top_frame, textvar=self.text_to_find)

        replace_entry_label = ttk.Label(middle_frame, text="Replace: ", style="editor.TLabel")
        self.replace_entry = ttk.Entry(middle_frame, textvar=self.text_to_replace_with)

        self.find_button = ttk.Button(bottom_frame, text="Find",
                                      command=self.on_find, style="editor.TButton")
        self.replace_button = ttk.Button(bottom_frame, text="Replace",
                                         command=self.on_replace, style="editor.TButton")

        find_entry_label.pack(side=tk.LEFT, padx=(20, 0))
        self.find_entry.pack(side=tk.LEFT, fill=tk.X, expand=1)

        replace_entry_label.pack(side=tk.LEFT)
        self.replace_entry.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.find_button.pack(side=tk.LEFT, padx=(85, 0))
        self.replace_button.pack(side=tk.LEFT, padx=(20, 20))

        top_frame.pack(side=tk.TOP, expand=1, fill=tk.X, padx=30)
        middle_frame.pack(side=tk.TOP, expand=1, fill=tk.X, padx=30)
        bottom_frame.pack(side=tk.TOP, expand=1, fill=tk.X)

        self.find_entry.focus_force()

    #查找
    def on_find(self):
        self.master.find(self.text_to_find.get())

    #替换
    def on_replace(self):
        '''
        @update 1.添加自动查找
        '''
        self.master.find(self.text_to_find.get())
        self.master.replace_text(self.text_to_find.get(), self.text_to_replace_with.get())
