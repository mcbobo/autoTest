# coding:utf-8
import os
import subprocess

from common.BasePickle import readInfo, write

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class WifiConnect:
    """
    adb无线连接多台Android设备
    连接一次设备后，保存设备ip到本地
    """

    def __init__(self):
        self.loc_pool = readInfo(PATH("../data/ip.pickle"))
        self.devices_list = []

    # adb无线连接设备
    def connect(self):
        port = 5555
        ipadress = self._ip()
        for i in ipadress:
            ip_port = i + ':' + str(port)
            cmd1 = "adb tcpip " + str(port)
            cmd2 = "adb connect " + ip_port
            print(cmd2)
            os.popen(cmd1)
            os.popen(cmd2)
            self.devices_list.append(ip_port)
        self.save_ip(ipadress)

    def disconnect(self):
        pass

    @staticmethod
    def save_ip(data):
        write(data, PATH("../data/ip.pickle"))

    def _ip(self):
        """
        获取设备ip地址
        :return: ip_pool
        """
        cmd = 'adb devices'
        ip_str = 'inet addr:'
        dev = os.popen(cmd).readlines()
        len_devices = len(dev) - 1
        for i in range(1, len_devices):
            ip_cmd = 'adb -s ' + dev[i].split('\t')[0] + ' shell ifconfig wlan0'
            ip_info = subprocess.Popen(ip_cmd, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).stdout.readlines()
            for line in ip_info:
                temp = line.decode().strip()
                if temp.find(ip_str) >= 0:
                    ip = temp[len(ip_str):].split()[0]
                    if ip not in self.loc_pool:
                        self.loc_pool.append(ip)
        return self.loc_pool


if __name__ == '__main__':
    WifiConnect().connect()
