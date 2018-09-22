#!python3
# coding:utf-8
from tkinter import *
import tkinter.messagebox
import tkinter as tk

import locateAlg
import wifiScan
import math


class mainDialog(object):
    def __init__(self, root, list):
        self.frame_left = Frame(root, padx=5)
        self.frame_right = Frame(root, padx=5)

        self.precision = 0.5  # 一格(20像素)代表1m
        self.myPoints = []  # 保存3个点的坐标
        self.dis = []  # 保存3个AP的实际半径
        self.radius = []  # 保存3个圆的半径

        '''
            the wight in the left:
            A label, a listbox, a button
        '''
        # lable
        Label(self.frame_left, text="Id".ljust(3) + "    " + "Name".ljust(20) + " " + "Signal".rjust(5)).pack()

        # listbox
        self.list = list
        self.name = StringVar()
        nameAndSignal = split(list)
        self.name.set(nameAndSignal)
        self.nameBox = Listbox(self.frame_left, listvariable=self.name, width=25, height=15, activestyle='none',
                               cursor='hand2',
                               highlightthickness=0, selectmode=tk.MULTIPLE)

        self.nameBox.pack(side=TOP)

        # detail
        self.frame_detail = Frame(self.frame_left)

        # Label(self.frame_left, text='选择的三个热点').pack()
        Label(self.frame_detail, text='①名 字:').grid(column=0, row=0, sticky=E)
        self.text_first_name = Text(self.frame_detail, height=1, width=17, state=DISABLED, bg='#F8F8F8',
                                    cursor='left_ptr')
        self.text_first_name.grid(column=1, row=0)
        Label(self.frame_detail, text='①MAC:').grid(column=0, row=1, sticky=E)
        self.text_first_mac = Text(self.frame_detail, height=1, width=17, state=DISABLED, bg='#F8F8F8',
                                   cursor='left_ptr')
        self.text_first_mac.grid(column=1, row=1)

        Label(self.frame_detail, text='②名 字:').grid(column=0, row=2, sticky=E)
        self.text_second_name = Text(self.frame_detail, height=1, width=17, state=DISABLED, bg='#F8F8F8',
                                     cursor='left_ptr')
        self.text_second_name.grid(column=1, row=2)
        Label(self.frame_detail, text='②MAC:').grid(column=0, row=3, sticky=E)
        self.text_second_mac = Text(self.frame_detail, height=1, width=17, state=DISABLED, bg='#F8F8F8',
                                    cursor='left_ptr')
        self.text_second_mac.grid(column=1, row=3)

        Label(self.frame_detail, text='③名 字:').grid(column=0, row=4, sticky=E)
        self.text_third_name = Text(self.frame_detail, height=1, width=17, state=DISABLED, bg='#F8F8F8',
                                    cursor='left_ptr')
        self.text_third_name.grid(column=1, row=4)
        Label(self.frame_detail, text='③MAC:').grid(column=0, row=5, sticky=E)
        self.text_third_mac = Text(self.frame_detail, height=1, width=17, state=DISABLED, bg='#F8F8F8',
                                   cursor='left_ptr')
        self.text_third_mac.grid(column=1, row=5)

        self.frame_detail.pack(side=TOP)

        # button
        Button(self.frame_left, text='刷 新', width=8, height=6, command=self.update).pack(side=TOP)

        self.frame_left.pack(side=LEFT)

        '''
            the wight in the left:
            A button, a text, a text
         '''

        Label(self.frame_right, text='定位信息').pack()
        self.scanText = Text(self.frame_right, height=2, pady=4, state=DISABLED, bg='#F8F8F8', cursor='left_ptr')
        self.setText(self.scanText, '请在左侧列表选择三个热点，然后按id次序在下图标出三个热点的位置，点击“定位”')
        self.scanText.pack(side=TOP)

        self.map = Canvas(self.frame_right, height=366, bg='#D9D9D9')

        # 画线，每20像素
        for i in range(0, 400, 20):
            self.map.create_line(0, i, 380, i, fill='gray', dash=(3, 5))
            self.map.create_line(i, 0, i, 380, fill='gray', dash=(3, 5))
        self.map.create_text(368, 355, text=str(self.precision)+'m')

        self.map.pack()

        # 画布与鼠标左键进行绑定
        self.map.bind("<Button-1>", self.paintPoint)
        self.drawPoints = 0

        Button(self.frame_right, text='定 位', width=8, command=self.locate).pack(side=TOP)

        self.frame_right.pack(side=RIGHT)


    def refreshList(self, wifilist_new, id=0):
        nameAndSignal_new = split(wifilist_new)

        self.nameBox.delete(0, len(self.list))

        self.list = wifilist_new
        self.name = StringVar()
        self.name.set(list)

        for wi in nameAndSignal_new:
            self.nameBox.insert(END, wi)

    def update(self):
        wifilist_new = wifiScan.scanWifi()
        self.refreshList(wifilist_new, id)
        for order in [self.text_first_name, self.text_second_name, self.text_third_name]:
            order.delete(1.0, END)
        for order in [self.text_first_mac, self.text_second_mac, self.text_third_mac]:
            order.delete(1.0, END)

        self.dis.clear()
        self.myPoints.clear()
        self.radius.clear()

        self.setText(self.scanText, '请在左侧列表选择三个热点，然后按id次序在下图标出三个热点的位置，点击“定位”')

        self.drawPoints = 0
        self.map.delete(ALL)
        # 画线
        for i in range(0, 400, 20):
            self.map.create_line(0, i, 380, i, fill='gray', dash=(3, 5))
            self.map.create_line(i, 0, i, 380, fill='gray', dash=(3, 5))
        self.map.create_text(368, 355, text=str(self.precision)+'m')

    def paintPoint(self, event):
        if len(self.nameBox.curselection()) != 3:
            tkinter.messagebox.showinfo('提示', '请在左侧列表选择三个热点')
        elif self.drawPoints >= 3:
            tkinter.messagebox.showinfo('提示', '只能标记三个点')
        else:
            self.myPoints.append({'x': event.x, 'y': event.y})
            x1, y1 = (event.x - 3), (event.y - 3)
            x2, y2 = (event.x + 3), (event.y + 3)
            self.map.create_oval(x1, y1, x2, y2, fill='red')
            self.drawPoints = self.drawPoints + 1
            # print(self.drawPoints, event.x, event.y)
            # print(self.myPoints[self.drawPoints-1]['x'])

    def paintCircle(self):
        for i in range(3):
            self.map.create_oval(self.myPoints[i]['x'] - self.radius[i], self.myPoints[i]['y'] - self.radius[i] \
                                 , self.myPoints[i]['x'] + self.radius[i], self.myPoints[i]['y'] + self.radius[i])

    def locate(self):
        selections = self.nameBox.curselection()
        if len(selections) != 3:
            tkinter.messagebox.showinfo('提示', '请在左侧列表选择三个热点')
        elif self.drawPoints != 3:
            tkinter.messagebox.showinfo('提示', '请标记三个热点的位置')
        else:
            for i, order in enumerate([self.text_first_name, self.text_second_name, self.text_third_name]):
                self.setText(order, self.list[selections[i]][0])
                disTemp = signalToDis(self.list[selections[i]][4])
                self.dis.append(disTemp)
                self.radius.append(disTemp/self.precision * 20)
            for i, order in enumerate([self.text_first_mac, self.text_second_mac, self.text_third_mac]):
                self.setText(order, self.list[selections[i]][1])

            self.setText(self.scanText, '距离三个热点的距离分别为%.2f米，%.2f米，%.2f米，如下图所示，黄点表示您当前位置' % (self.dis[0], self.dis[1], self.dis[2]))

            self.paintCircle()

            # 定位
            xc, yc = locateAlg.intersection(self.myPoints, self.radius)
            if xc == -1 and yc == -1:
                tkinter.messagebox.showinfo('错误', '定位错误，可能是因为热点位置标记错误，或者是信号强度探测有误，请刷新后重试！')
            else:
                x1, y1 = (xc - 3), (yc - 3)
                x2, y2 = (xc + 3), (yc + 3)
                self.map.create_oval(x1, y1, x2, y2, fill='yellow')

    def setText(self, widget, text):
        widget.config(state=NORMAL)
        widget.delete(1.0, END)
        widget.insert(1.0, text)
        widget.config(state=DISABLED)


def textLength(text, width):
    length = len(text)
    if (length > width - 2):
        text = text[0:width - 2]
    else:
        text = text + (width - length) * " "

    return text


def signalToDis(sig):
    A = 46
    n = 4.0
    return 10 ** ((-int(sig) - A) / (10 * n))


def split(list):
    nameAndSignal = []
    for id, l in enumerate(list):
        temp = textLength(str(id), 5) + textLength(l[0], 20) + textLength(l[4], 6)
        print(temp)
        nameAndSignal.append(temp)

    return nameAndSignal


if __name__ == '__main__':
    wifilist = wifiScan.scanWifi()

    root = Tk()
    root.title("WIFI")
    root.geometry("580x468")
    root.resizable(width=False, height=False)

    mainDialog(root, wifilist)
    root.mainloop()
