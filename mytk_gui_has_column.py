from tkinter import Tk, Frame, StringVar, messagebox, ttk
from tkinter import Button, Entry, Canvas, Label
from wifi_conect_class import MyWifiCrack
import time
import pywifi


soft_tkwidth = 350
soft_tkheight = 350
soft_tk_title = '获取WIFI密码'



class WiFiCrack(object):
    def __init__(self):
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
        self.flef = Frame(self.win)
        self.flef.pack(side='left')
        self.frig = Frame(self.win)
        self.frig.pack(side='right')
        self.fbot = Frame(self.win)
        self.fbot.pack(side='bottom')

        tree_columns = ('order', 'wifi_name', 'signal_strength')
        self.tree = ttk.Treeview(self.flef, show='headings', columns=tree_columns)
        
        self.tree.column('order', width=50)
        self.tree.column('wifi_name', width=150)
        self.tree.column('signal_strength', width=80)
        self.tree.heading('order', text='序号')
        self.tree.heading('wifi_name', text='WiFi名称')
        self.tree.heading('signal_strength', text='信号强度')
        self.tree.pack()

        self.but0 = Button(self.frig, text='显示WIFI', command=self.check_wifi_module)
        self.but1 = Button(self.frig, text='点击获取', command=self.get_password)
        self.but2 = Button(self.frig, text='取消获取', command=self.cancel_get_password)
        self.but3 = Button(self.frig, text='退出', command=self.win.quit)
        self.but0.pack()
        self.but1.pack()
        self.but2.pack()
        self.but3.pack()

        self.lb2 = Label(self.ftop, text='密码：')
        self.lb2.grid(row=0, column=0)
        self.ent1 = Entry(self.ftop, textvariable=self.e1_str)
        self.ent1.grid(row=0, column=1)


        self.cv1 = Canvas(self.ftop, width=150, height=24, bg='white')
        self.cv1.grid(row=1, column=0)
        self.lb1 = Label(self.ftop, textvariable=self.l1_str, width=5, height=1, bg='white')
        self.lb1.grid(row=1, column=1)

        
        
        


    def get_password(self):
        max_num = 600
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
        for i in range(max_num):
            time.sleep(0.1)
            self.change_schedule(i, max_num-1)
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
        warn_has_wifi_module_msg = '该电脑存在无线网卡模块，可以尝试获取密码！'
        if wireless_lists == []:
            messagebox.showwarning(warn_title, warn_no_wifi_module_msg)
        else:
            messagebox.showwarning(warn_title, warn_has_wifi_module_msg)
            
            

    def show(self):
        self.win.mainloop()


if __name__ == "__main__":
    wk = WiFiCrack()
    wk.show()

