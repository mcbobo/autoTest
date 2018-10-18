# coding:utf-8
import os
import multiprocessing
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
    lock = multiprocessing.Lock()

    def __init__(self):
        self.ip_data = readInfo(PATH("../data/ip.pickle"))
        self.ipPort_pool = []
        # self.lock = multiprocessing.Lock()

    # 多线程无线连接设备
    def connect_syc(self):
        ip_port_pool = self._ip_port()
        num = len(ip_port_pool) if len(ip_port_pool) < 5 else 5

        if num > 0:
            pool = multiprocessing.Pool(processes=num)
            pool.map(self.connect, ip_port_pool)
            print(self.ip_data)
            print("start saving")
            self.save_ip(self.ip_data)
        else:
            print("没有可用的安卓设备")

    # adb无线连接设备
    def connect(self, ip_port):
        temp = ip_port.split(':')
        port = temp[-1]
        ip = temp[0]
        cmd1 = "adb tcpip " + str(port)
        cmd2 = "adb connect " + ip_port

        os.popen(cmd1)
        status = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
        # os.popen(cmd2)
        if status[0].decode().find("connected"):
            print("connected to %s" % ip_port)
        else:
            # self.lock.acquire()
            print("unable to connect to %s" % ip_port)
            self._remove(ip)
            print(self.ip_data)
            # self.lock.release()

    def disconnect(self, ip_port):
        cmd = "adb disconnect " + ip_port
        status = os.popen(cmd)
        if status.find("disconnected"):
            print("disconnected %s" % ip_port)
        else:
            print(status)

    @staticmethod
    def save_ip(data):
        write(data, PATH("../data/ip.pickle"))

    def _remove(self, data):
        self.ip_data.remove(data)

    def _ip_port(self):
        ip_pool = self._ip()
        port = 5555
        for i in ip_pool:
            ip_port = i + ':' + str(port)
            self.ipPort_pool.append(ip_port)
            port += 2
        return self.ipPort_pool

    def _ip(self):
        """
        获取设备ip地址
        :return: run_pool
        """
        ip_pool = []
        cmd = 'adb devices'
        ip_str = 'inet addr:'
        dev = os.popen(cmd).readlines()
        len_devices = len(dev) - 1

        if len_devices > 1:
            for i in range(1, len_devices):
                ip_cmd = 'adb -s ' + dev[i].split('\t')[0] + ' shell ifconfig wlan0'
                ip_info = subprocess.Popen(ip_cmd, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE).stdout.readlines()
                for line in ip_info:
                    temp = line.decode().strip()
                    if temp.find(ip_str) >= 0:
                        ip = temp[len(ip_str):].split()[0]
                        ip_pool.append(ip)
                        if ip not in self.ip_data:
                            self.ip_data.append(ip)
            run_pool = list(filter(lambda x: x not in ip_pool, self.ip_data))
            return run_pool
        else:
            run_pool = self.ip_data
            return run_pool


if __name__ == '__main__':
    # WifiConnect().connect_syc()
    WifiConnect()._ip()
