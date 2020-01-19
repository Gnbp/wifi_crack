from tkinter import Tk, Frame, StringVar, messagebox
from tkinter import Button, Entry, Canvas, Label
from wifi_conect_class import MyWifiCrack
import time
import pywifi
import os


soft_tkwidth = 290
soft_tkheight = 90
soft_tk_title = '获取WIFI密码'

base_password_filepath = os.path.join(os.path.split(__file__)[0], 'new_password_lists.txt')



class WiFiCrack(object):
    def __init__(self, password_filepath):
        self.password_filepath = password_filepath
        self.win = Tk()
        self.win.title(soft_tk_title)
        soft_tk_x = int((self.win.winfo_screenwidth()-soft_tkwidth)/2)
        soft_tk_y = int((self.win.winfo_screenheight()-soft_tkheight)/2)
        soft_tk_size = '{}x{}+{}+{}'.format(
            soft_tkwidth, 
            soft_tkheight, 
            soft_tk_x, 
            soft_tk_y)
        self.win.geometry(soft_tk_size)
        self.e1_str = StringVar()
        self.l1_str = StringVar()
        self.cancel_flag = False
        self.canvas_posx = (5, 5) 
        self.canvas_posy = (5, 24)


        self.ftop = Frame(self.win)
        self.ftop.pack(side='top')
        self.fcen = Frame(self.win)
        self.fcen.pack()
        self.fbot = Frame(self.win)
        self.fbot.pack(side='bottom')


        self.cv1 = Canvas(self.ftop, width=150, height=24, bg='white')
        self.cv1.pack(side='left')
        self.lb1 = Label(self.ftop, textvariable=self.l1_str, width=5, height=1, bg='white')
        self.lb1.pack(side='right')

        self.lb2 = Label(self.fcen, text='密码：')
        self.lb2.pack(side='left')
        self.ent1 = Entry(self.fcen, textvariable=self.e1_str, width=30)
        self.ent1.pack(side='right')
        
        self.but0 = Button(self.fbot, text='检查无线网卡', command=self.check_wifi_module)
        self.but1 = Button(self.fbot, text='点击获取', command=self.get_password)
        self.but2 = Button(self.fbot, text='取消获取', command=self.cancel_get_password)
        self.but3 = Button(self.fbot, text='退出', command=self.win.quit)
        self.but0.pack(side='left')
        self.but1.pack(side='left', anchor='w')
        self.but2.pack(side='left')
        self.but3.pack(side='right', anchor='e')

    def get_password_lists(self):
        with open(self.password_filepath, 'r') as fr:
            password_lists = fr.readlines()
        return password_lists

    def get_password(self):
        wifi_obj = pywifi.PyWiFi()
        wireless_lists = wifi_obj.interfaces()
        if wireless_lists != []:
            wireless_obj = wireless_lists[0]
            profile_obj = pywifi.Profile()
            self.password_lists = self.get_password_lists()
            wifi_crack = MyWifiCrack(wireless_obj, profile_obj)

            # 填充进度条
            self.out_rec = self.cv1.create_rectangle(
                self.canvas_posx[0],
                self.canvas_posx[1],
                self.canvas_posy[0]+100,
                self.canvas_posy[1],
                outline = "green",width = 1)
            self.fill_rec = self.cv1.create_rectangle(
                self.canvas_posx[0],
                self.canvas_posx[1],
                self.canvas_posy[0],
                self.canvas_posy[1],outline = "",width = 0,fill = "green")

            for i in range(len(self.password_lists)):
                time.sleep(0.1)
                wifi_crack.run_password_str(self.password_lists[i])
                self.change_schedule(i, len(self.password_lists)-1)
                if self.cancel_flag:
                    self.l1_str.set('')
                    break


    #更新进度条函数
    def change_schedule(self, now_schedule, all_schedule):
        self.cv1.coords(self.fill_rec, (
            self.canvas_posx[0],
            self.canvas_posx[1],
            self.canvas_posy[0]+1+(now_schedule/all_schedule)*100,
            self.canvas_posy[1]))
        self.ftop.update()
        self.l1_str.set(str(round(now_schedule/all_schedule*100, 2)) + '%')
        if round(now_schedule/all_schedule*100, 2) == 100.00:
            self.l1_str.set("完成")
    
    def cancel_get_password(self):
        self.cv1.delete(self.out_rec)
        self.cv1.delete(self.fill_rec)
        self.l1_str.set('')
        self.cancel_flag = True

    def check_wifi_module(self):
        wifi_obj = pywifi.PyWiFi()
        wireless_lists = wifi_obj.interfaces()
        warn_title = '警告'
        warn_no_wifi_module_msg = '该电脑没有无线网卡模块！'
        
        warn_has_wifi_module_msg = '该电脑存在无线网卡模块，可以吃尝试获取密码！'
        if wireless_lists == []:
            messagebox.showwarning(warn_title, warn_no_wifi_module_msg)
        else:
            messagebox.showwarning(warn_title, warn_has_wifi_module_msg)
            

    def show(self):
        self.win.mainloop()


if __name__ == "__main__":
    
    wk = WiFiCrack(base_password_filepath)
    wk.show()

