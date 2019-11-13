# -*- coding: utf-8 -*-
# @Date    : 2018-10-30
# @Author  : Don't know
# @Editor  : 黄炫智 耿晟昶

import tkinter as tk
import tkinter.messagebox as msg

#文本框
class TextArea(tk.Text):

    #初始化函数
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)

        self.master = master
        self.visibles = True

        self.config(wrap='none')  # CHAR NONE

        self.tag_configure('find_match', background="yellow")
        self.tag_configure('focus_line', background='#CCCCCC')
        self.find_text = ""
        self.find_match_index = None
        self.find_search_starting_index = 1.0

        self.bind_events()

    #绑定事件
    def bind_events(self):
        self.bind('<Control-a>', self.select_all)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-v>', self.paste)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-y>', self.redo)
        self.bind('<Control-z>', self.undo)
        self.bind('<Motion>', self.focus_background)

    #剪切
    def cut(self, event=None):
        self.event_generate("<<Cut>>")
        self.master.line_numbers.force_update()
        return "break"

    #复制
    def copy(self, event=None):
        self.event_generate("<<Copy>>")
        self.master.line_numbers.force_update()
        return "break"

    #粘贴
    def paste(self, event=None):
        self.event_generate("<<Paste>>")
        self.master.line_numbers.force_update()
        return "break"

    #撤销
    def undo(self, event=None):
        self.event_generate("<<Undo>>")
        self.master.line_numbers.force_update()
        return "break"

    #重复
    def redo(self, event=None):
        self.event_generate("<<Redo>>")
        self.master.line_numbers.force_update()
        return "break"

    #全选
    def select_all(self, event=None):
        self.tag_add("sel", 1.0, tk.END)
        return "break"

    #内容搜索
    def find(self, text_to_find):
        '''
        @param text_to_find: 查找的文字
        @update 1.添加搜索内容变换检测 2.同种提示信息同时只会显示一个 3.不在自动换行
        '''
        length = tk.IntVar()
        if(text_to_find != self.find_text):
            self.find_text = text_to_find
            self.find_search_starting_index = 1.0
            self.find_match_index = None
        idx = self.search(text_to_find, self.find_search_starting_index,
                          stopindex=tk.END, count=length)

        if idx:
            self.tag_remove('find_match', 1.0, tk.END)
            print(length.get())
            end = f'{idx}+{length.get()}c'
            print(idx, end)
            self.tag_add('find_match', idx, end)
            self.see(idx)

            self.find_search_starting_index = end
            self.find_match_index = idx
        else:
            if self.find_match_index != None:
                if self.visibles:
                    self.visibles = False
                    if msg.askyesno("No more results",
                                    "No further matches. Repeat from the beginning?"):
                        self.find_search_starting_index = 1.0
                        self.find_match_index = None
                        self.visibles = True
                        return self.find(text_to_find)
                    else:
                        self.visibles = True
            else:
                if self.visibles:
                    self.visibles = False
                    if (msg.showinfo("No Matches", "No matching text found")):
                        self.visibles = True
                    else:
                        self.visibles = True
        self.focus_background()

    #当前行背景
    def focus_background(self, event=None):
        self.tag_remove('focus_line', 1.0, "end")
        self.tag_add('focus_line', "current linestart", "current lineend+1c")

    #替换文本
    def replace_text(self, target, replacement):
        '''
        @param target: 替换目标
        @param replacement: 替换内容
        '''
        if self.find_match_index:
            current_found_index_line = str(self.find_match_index).split('.')[0]

            end = f"{self.find_match_index}+{len(target)}c"
            self.replace(self.find_match_index, end, replacement)

            self.find_search_starting_index = current_found_index_line + '.0'

    #移除查找标签
    def cancel_find(self):
        self.find_search_starting_index = 1.0
        self.find_match_index = None
        self.tag_remove('find_match', 1.0, tk.END)

    #载入文档
    def display_file_contents(self, filepath):
        '''
        @param filepath: 文档文件路径
        '''
        with open(filepath, 'r') as file:
            self.delete(1.0, tk.END)
            self.insert(1.0, file.read())


