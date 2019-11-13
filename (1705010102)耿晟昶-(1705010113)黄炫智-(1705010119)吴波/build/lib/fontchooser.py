# -*- coding: utf-8 -*-
# @Date    : 2018-10-30
# @Author  : Don't know
# @Editor  : 黄炫智 耿晟昶

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import families

#字体字号选择窗口
class FontChooser(tk.Toplevel):

    #初始化字体选择窗口
    def __init__(self, master, **kwargs):
        '''
        @update 1.增加无效值检查
        '''
        super().__init__(**kwargs)
        self.master = master
        self.vss = tk.IntVar()
        self.vss.set(self.master.font_size)

        self.transient(self.master)
        self.geometry('500x250')
        self.title('Choose font and size')

        self.configure(bg=self.master.background)

        self.font_list = tk.Listbox(self, exportselection=False)

        self.available_fonts = sorted(families())

        for family in self.available_fonts:
            self.font_list.insert(tk.END, family)

        if self.master.font_family not in self.available_fonts:
            current_selection_index = 1
        else:
            current_selection_index = self.available_fonts.index(self.master.font_family)
        if current_selection_index:
            self.font_list.select_set(current_selection_index)
            self.font_list.see(current_selection_index)

        self.size_input = tk.Spinbox(self, from_=0, to=99, textvariable=self.vss)

        self.save_button = ttk.Button(self, text="Save", style="editor.TButton", command=self.save)

        self.save_button.pack(side=tk.BOTTOM, fill=tk.X, expand=1, padx=40)
        self.font_list.pack(side=tk.LEFT, fill=tk.Y, expand=1)
        self.size_input.pack(side=tk.BOTTOM, fill=tk.X, expand=1)

    #保存字体修改并应用
    def save(self):
        '''
        @update 1.去除无效的'@'符号
        '''
        font_family = self.font_list.get(self.font_list.curselection()[0]).replace("@", "")
        yaml_file_contents = f"family: {font_family}\n" \
                           + f"size: {self.size_input.get()}"

        with open(self.master.font_scheme_path, 'w') as file:
            file.write(yaml_file_contents)

        self.master.update_font()
        self.destroy()

