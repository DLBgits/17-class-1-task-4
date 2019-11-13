# -*- coding: utf-8 -*-
# @Date    : 2018-10-30
# @Author  : Don't know
# @Editor  : 黄炫智 耿晟昶

import tkinter as tk

#行号
class LineNumbers(tk.Text):

    masters = None
    texts = None
    liness = None

    #初始化
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)
        self.masters = text_widget
        self.mains = master

        self.text_widget = text_widget
        self.text_widget.bind('<Key>', self.on_key_press)

        self.insert(1.0, '1')
        self.configure(state='disabled')

    #每次按键触发，检查行号
    def on_key_press(self, event=None):
        '''
        @update 1.修正行号 2.修正键入时跳转文字会使行号不正确
        '''
        self.texts = self.masters.get("0.0", "end")
        self.liness = self.texts.split('\n')
        if event == None:
            num_of_lines = len(self.liness)-1
        else:
            if(event.keysym == "Return"):
                num_of_lines = len(self.liness)
            else:
                if(event.keysym == "BackSpace"):
                    num_of_lines = len(self.liness)-1
                    cur = self.masters.index("insert")
                    if(int(cur.split('.')[0]) >= 2 and
                       self.masters.get("{}.end".format(int(cur.split('.')[0]) - 1), "insert") == "\n"):
                        num_of_lines = len(self.liness)-2
                else: 
                    if(event.keysym == "Delete"):
                        num_of_lines = len(self.liness)-1
                        cur = self.masters.index("insert")
                        if(int(cur.split('.')[0]) < num_of_lines and
                           self.masters.get("insert", "{}.end".format(int(cur.split('.')[0]))) == ""):
                            num_of_lines = len(self.liness)-2
                    else:
                        num_of_lines = len(self.liness)-1
        line_numbers_string = "\n".join(str(no + 1) for no in range(int(num_of_lines)))
        width = len(str(num_of_lines))

        self.configure(state='normal', width=width)
        self.delete(1.0, tk.END)
        self.insert(1.0, line_numbers_string)
        self.configure(state='disabled')

        self.yview("moveto", self.masters.yview()[0])

        self.mains.highlighter.clear_highlight()
        self.mains.highlighter.force_highlight()
        self.masters.cancel_find()

    #行号更新
    def force_update(self):
        self.on_key_press()
