# -*- coding: utf-8 -*-
# @Date    : 2018-10-30
# @Author  : Don't know
# @Editor  : 黄炫智 耿晟昶

import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from pathlib import Path
from tkinter import filedialog

import yaml

from textarea import TextArea
from linenumbers import LineNumbers
from highlighter import Highlighter
from findwindow import FindWindow
from colourchooser import ColourChooser
from fontchooser import FontChooser

#主程序
class MainWindow(tk.Tk):
    '''
    @param tk.TK: Windows、Mac、Unix下TK GUI套件的标准Python接口，可实现GUI界面
    '''

    #窗口设置
    def __init__(self):
        '''
        @update 1.添加横向滚动条 2.修正行号与滚动条和窗口的关联 3.修正行号显示
        '''
        super().__init__()

        self.title('Python Text Editor v3')
        self.geometry('800x600')

        self.foreground = 'black'
        self.background = 'lightgrey'
        self.text_foreground = 'black'
        self.text_background = 'white'

        self.config_dir = os.path.join(str(Path.home()), '.tkedit')

        self.default_scheme_path = os.path.join(self.config_dir, 'schemes/default.yaml')
        self.python_language_path = os.path.join(self.config_dir, 'languages/python.yaml')
        self.none_language_path = os.path.join(self.config_dir, 'languages/None.yaml')
        self.font_scheme_path = os.path.join(self.config_dir, 'fonts/font.yaml')
        self.create_config_directory_if_needed()

        self.load_scheme_file(self.default_scheme_path)
        self.configure_ttk_elements()

        self.font_size = 15
        self.font_family = "Ubuntu Mono"
        self.load_font_file(self.font_scheme_path)

        self.text_area = TextArea(self, bg=self.text_background, fg=self.text_foreground, undo=True,
                                  font=(self.font_family, self.font_size))

        self.scrollbar = ttk.Scrollbar(orient="vertical", command=self.text_area.yview)
        self.scrollbar2 = ttk.Scrollbar(orient="horizontal", command=self.text_area.xview)

        self.line_numbers = LineNumbers(self, self.text_area, bg="grey", fg="white", width=1,
                                        font=(self.font_family, self.font_size))
        self.scrollbar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scrollbar.set, xscrollcommand=self.scrollbar2.set)
        self.highlighter = Highlighter(self.text_area, self.none_language_path)

        self.menu = tk.Menu(self, bg=self.background, fg=self.foreground)
        self.all_menus = [self.menu]

        sub_menu_items = ["file", "edit", "tools", "help"]
        self.generate_sub_menus(sub_menu_items)
        self.configure(menu=self.menu)

        self.right_click_menu = tk.Menu(self, bg=self.background, fg=self.foreground, tearoff=0)
        self.right_click_menu.add_command(label='Cut', command=self.edit_cut)
        self.right_click_menu.add_command(label='Copy', command=self.edit_copy)
        self.right_click_menu.add_command(label='Paste', command=self.edit_paste)
        self.all_menus.append(self.right_click_menu)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar2.pack(side=tk.BOTTOM, fill=tk.X)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.bind_events()

        self.open_file = ''

    #绑定事件
    def bind_events(self):
        self.text_area.bind("<MouseWheel>", self.scroll_text)
        self.text_area.bind("<Button-4>", self.scroll_text)
        self.text_area.bind("<Button-5>", self.scroll_text)
        self.text_area.bind("<Button-3>", self.show_right_click_menu)

        self.bind('<Control-f>', self.show_find_window)

        self.bind('<Control-n>', self.file_new)
        self.bind('<Control-o>', self.file_open)
        self.bind('<Control-s>', self.file_save)

        self.bind('<Control-h>', self.help_about)

        self.bind('<Control-m>', self.tools_change_syntax_highlighting)
        self.bind('<Control-g>', self.tools_change_colour_scheme)
        self.bind('<Control-l>', self.tools_change_font)

        self.line_numbers.bind("<MouseWheel>", lambda e: "break")
        self.line_numbers.bind("<Button-4>", lambda e: "break")
        self.line_numbers.bind("<Button-5>", lambda e: "break")

    #滚动事件
    def scroll_text(self, *args):
        if len(args) > 1:
            self.text_area.yview_moveto(args[1])
            self.line_numbers.yview_moveto(args[1])
        else:
            event = args[0]
            if event.delta:
                move = -1 * (event.delta / 120)
            else:
                if event.num == 5:
                    move = 1
                else:
                    move = -1

            self.text_area.yview_scroll(int(move), "units")
            self.line_numbers.yview_scroll(int(move) * 3, "units")

    #内容查找、替换窗口
    def show_find_window(self, event=None):
        FindWindow(self.text_area)

    #显示右键菜单
    def show_right_click_menu(self, event):
        x = self.winfo_x() + self.text_area.winfo_x() + event.x
        y = self.winfo_y() + self.text_area.winfo_y() + event.y
        self.right_click_menu.post(x, y)

    #设置子菜单
    def generate_sub_menus(self, sub_menu_items):
        '''
        @param sub_menu_items: 子菜单项目
        '''
        window_methods = [method_name for method_name in dir(self)
                          if callable(getattr(self, method_name))]
        tkinter_methods = [method_name for method_name in dir(tk.Tk)
                           if callable(getattr(tk.Tk, method_name))]

        my_methods = [method for method in set(window_methods) - set(tkinter_methods)]
        my_methods = sorted(my_methods)

        for item in sub_menu_items:
            sub_menu = tk.Menu(self.menu, tearoff=0, bg=self.background, fg=self.foreground)
            matching_methods = []
            for method in my_methods:
                if method.startswith(item):
                    matching_methods.append(method)

            for match in matching_methods:
                actual_method = getattr(self, match)
                method_shortcut = actual_method.__doc__.strip()
                friendly_name = ' '.join(match.split('_')[1:])
                sub_menu.add_command(label=friendly_name.title(), command=actual_method,
                                     accelerator=method_shortcut)

            self.menu.add_cascade(label=item.title(), menu=sub_menu)
            self.all_menus.append(sub_menu)

    #显示关于
    def show_about_page(self):
        msg.showinfo("About", "My text editor, version 2, written in Python3.6 using tkinter!")

    #加载文字高亮配色方案
    def load_syntax_highlighting_file(self):
        syntax_file = filedialog.askopenfilename(filetypes=[("YAML file", ("*.yaml", "*.yml"))])
        if syntax_file:
            self.highlighter.clear_highlight()
            self.highlighter = Highlighter(self.text_area, syntax_file)
            self.highlighter.force_highlight()

    #加载窗体配色方案
    def load_scheme_file(self, scheme):
        '''
        @param scheme: 目标配置文件
        @update GSC 预检测
        '''
        with open(scheme, 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as error:
                print(error)
                return

        if 'foreground' in config:
            self.foreground = config['foreground']
        if 'background' in config:
            self.background = config['background']
        if 'text_foreground' in config:
            self.text_foreground = config['text_foreground']
        if 'text_background' in config:
            self.text_background = config['text_background']

    #加载字体及字号方案
    def load_font_file(self, file_path):
        '''
        @param file_path: 方案存放路径及文件名
        '''
        with open(file_path, 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as error:
                print(error)
                return

        if 'family' in config:
            self.font_family = config['family']
        if 'size' in config:
            self.font_size = config['size']

    #修改窗体配色方案
    def change_colour_scheme(self):
        ColourChooser(self)

    #应用窗体配色方案
    def apply_colour_scheme(self, foreground, background, text_foreground, text_background):
        '''
        @param foreground: 新窗体前景色
        @param background: 新窗体背景色
        @param text_foreground: 新字体前景色
        @param text_background: 新字体背景色
        '''
        self.text_area.configure(fg=text_foreground, bg=text_background)
        self.background = background
        self.foreground = foreground
        for menu in self.all_menus:
            menu.configure(bg=self.background, fg=self.foreground)
        self.configure_ttk_elements()

    #应用按钮、标签配色方案
    def configure_ttk_elements(self):
        style = ttk.Style()
        style.configure('editor.TLabel', foreground=self.foreground, background=self.background)
        style.configure('editor.TButton', foreground=self.foreground, background=self.background)

    #字体选择窗口
    def change_font(self):
        FontChooser(self)

    #更新字体
    def update_font(self):
        '''
        @update 1.添加行号字体更新
        '''
        self.load_font_file(self.font_scheme_path)
        self.text_area.configure(font=(self.font_family, self.font_size))
        self.line_numbers.configure(font=(self.font_family, self.font_size))

    #运行环境检测
    def create_config_directory_if_needed(self):
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)
        if not os.path.exists(os.path.join(self.config_dir, 'schemes')):
            os.mkdir(os.path.join(self.config_dir, 'schemes'))
        if not os.path.exists(os.path.join(self.config_dir, 'languages')):
            os.mkdir(os.path.join(self.config_dir, 'languages'))
        if not os.path.exists(os.path.join(self.config_dir, 'fonts')):
            os.mkdir(os.path.join(self.config_dir, 'fonts'))

        self.create_default_scheme_if_needed()
        self.create_font_scheme_if_needed()
        self.create_python_language_if_needed()

    #运行环境创建 -- 窗体默认配置方案
    def create_default_scheme_if_needed(self):
        if not os.path.exists(self.default_scheme_path):
            yaml_file_contents = f"background: 'lightgrey'\n" \
                               + f"foreground: 'black'\n" \
                               + f"text_background: 'white'\n" \
                               + f"text_foreground: 'black'\n"

            with open(self.default_scheme_path, 'w') as yaml_file:
                yaml_file.write(yaml_file_contents)

    #运行环境创建 -- 字体默认配置方案
    def create_font_scheme_if_needed(self):
        if not os.path.exists(self.font_scheme_path):
            yaml_file_contents = f"family: Ubuntu Mono\n" \
                               + f"size: 15"

            with open(self.font_scheme_path, 'w') as yaml_file:
                yaml_file.write(yaml_file_contents)

    #运行环境创建 -- 语言文字高亮默认配置方案
    def create_python_language_if_needed(self):
        if not os.path.exists(self.python_language_path):
            yaml_file_contents = """
categories:
  keywords:
    colour: orange
    matches: [for, def, while, from, import, as, with, self]

  variables:
    colour: red4
    matches: ['True', 'False', None]

  conditionals:
    colour: green
    matches: [try, except, if, else, elif]

  functions:
    colour: blue4
    matches: [int, str, dict, list, set, float]

numbers:
  colour: purple

strings:
  colour: '#e1218b'
"""
            with open(self.python_language_path, 'w') as yaml_file:
                yaml_file.write(yaml_file_contents)

        if not os.path.exists(self.none_language_path):
            yaml_file_contents = """

categories:
  keywords:
    colour: black
    matches: [for, def, while, from, import, as, with, self]

  variables:
    colour: black
    matches: ['True', 'False', None]

  conditionals:
    colour: black
    matches: [try, except, if, else, elif]

  functions:
    colour: black
    matches: [int, str, dict, list, set, float]

numbers:
  colour: black

strings:
  colour: black
"""
            with open(self.none_language_path, 'w') as yaml_file:
                yaml_file.write(yaml_file_contents)






    # =========== Menu Functions ==============

    #新建文件
    def file_new(self, event=None):
        """
        Ctrl+N
        """
        self.text_area.delete(1.0, tk.END)
        self.open_file = ""
        self.line_numbers.force_update()

    #打开文件
    def file_open(self, event=None):
        """
        Ctrl+O
        """
        file_to_open = filedialog.askopenfilename()
        if file_to_open:
            self.open_file = file_to_open

            self.text_area.display_file_contents(file_to_open)
            self.highlighter.force_highlight()
            self.line_numbers.force_update()

    #保存文件
    def file_save(self, event=None):
        """
        Ctrl+S
        """
        current_file = self.open_file if self.open_file else None
        if not current_file:
            current_file = filedialog.asksaveasfilename()

        if current_file:
            contents = self.text_area.get(1.0, tk.END)
            with open(current_file, 'w') as file:
                file.write(contents)

    #剪切
    def edit_cut(self, event=None):
        """
        Ctrl+X
        """
        self.text_area.event_generate("<Control-x>")
        self.line_numbers.force_update()

    #粘贴
    def edit_paste(self, event=None):
        """
        Ctrl+V
        """
        self.text_area.event_generate("<Control-v>")
        self.line_numbers.force_update()
        self.highlighter.force_highlight()

    #复制
    def edit_copy(self, event=None):
        """
        Ctrl+C
        """
        self.text_area.event_generate("<Control-c>")

    #全选
    def edit_select_all(self, event=None):
        """
        Ctrl+A
        """
        self.text_area.event_generate("<Control-a>")

    #查找和替换
    def edit_find_and_replace(self, event=None):
        """
        Ctrl+F
        """
        self.show_find_window()

    #帮助与关于
    def help_about(self, event=None):
        """
        Ctrl+H
        """
        self.show_about_page()

    #选择语言（文字高亮）
    def tools_change_syntax_highlighting(self, event=None):
        """
        Ctrl+M
        """
        self.load_syntax_highlighting_file()

    #选择窗体配色
    def tools_change_colour_scheme(self, event=None):
        """
        Ctrl+G
        """
        self.change_colour_scheme()

    #选择字体字号
    def tools_change_font(self, event=None):
        """
        Ctrl+L
        """
        self.change_font()

    #主函数
def main():
    mw = MainWindow()
    mw.mainloop()

    #主过程
if __name__ == '__main__':
    main()
