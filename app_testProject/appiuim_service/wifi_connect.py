# coding:utf-8
import os
import socket
import multiprocessing
import subprocess

from common.BasePickle import read, write

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class WifiConnect:
    """
    adb无线连接多台Android设备
    连接一次设备后，保存设备ip到本地
    ipPort_pool:新增的设备
    run_pool:需要无线连接的设备
    ip_data:本地已保存的设备
    """
    lock = multiprocessing.Lock()

    def __init__(self):
        self.ip_data = read(PATH("../data/ip.pickle"))
        self.ipPort_pool = {}
        self.save_pool = []
        # self.lock = multiprocessing.Lock()

    # 多线程无线连接设备
    def connect_syc(self):
        run_pool = self._ip()
        num = len(run_pool) if len(run_pool) < 5 else 5

        if num > 0:
            pool = multiprocessing.Pool(processes=num)
            run_list = list(run_pool.values())
            pool.map(self.connect, run_list)
            # print(self.ipPort_pool)
            self.ipPort_pool.update(run_pool)
            print(self.ipPort_pool)
            print("start saving")
            self.save_ip(self.ipPort_pool)
        else:
            print("没有可用的安卓设备")

    # adb无线连接设备
    def connect(self, ip_port):
        temp = ip_port.split(':')
        port = temp[-1]
        ip = temp[0]
        cmd1 = "adb tcpip " + str(port)
        cmd2 = "adb connect " + ip_port

        if self.check_port(ip, int(port)) is False:
            os.popen(cmd2)
        else:
            os.popen(cmd1)
            status = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).stdout.readlines()
            if status[0].decode().find("connected"):
                print("connected to %s" % ip_port)
            else:
                # self.lock.acquire()
                print("unable to connect to %s" % ip_port)
                self._remove(ip_port)
                print(self.ip_data)
                # self.lock.release()

    @staticmethod
    def check_port(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((host, port))
            s.shutdown(2)
        except OSError:
            print('port %s is available!' % port)
            return True
        else:
            print('port %s already be in use! ' % port)
            return False

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
        for i in self.ip_data:
            if self.ip_data[i] == data:
                print('delete %s' % self.ip_data.pop(i))
                break

    # 弃用
    # def _ip_port(self, ip_pool):
    #     port_pool = [x.split(':')[-1] for x in self.ip_data]
    #     port = int(max(port_pool))
    #     for i in ip_pool:
    #         port += 2
    #         ip_port = i + ':' + str(port)
    #         self.ipPort_pool.append(ip_port)
    #
    #     return self.ipPort_pool

    def _ip(self):
        """
        获取设备ip地址
        :return: run_pool
        """
        exist_pool = ["port"]
        cmd = 'adb devices'
        ip_str = 'inet addr:'
        dev = os.popen(cmd).readlines()
        len_devices = len(dev) - 1
        port = self.ip_data.get("port", 5555)

        if len_devices > 1:
            for d in range(1, len_devices):
                uid = dev[d].split('\t')[0]
                if self.ip_data.get(uid):
                    exist_pool.append(uid)
                    print("本地已存该设备")
                elif uid in self.ip_data.values():
                    pass
                else:
                    ip_cmd = 'adb -s ' + uid + ' shell ifconfig wlan0'
                    ip_info = subprocess.Popen(ip_cmd, shell=True, stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE).stdout.readlines()
                    for line in ip_info:
                        temp = line.decode().strip()
                        if temp.find(ip_str) >= 0:
                            ip = temp[len(ip_str):].split()[0]
                            ip_port = ip + ':' + str(port)
                            print('ipPort')
                            self.ipPort_pool[uid] = ip_port
                            port += 2
                            #if d == len_devices - 1:
                            self.ipPort_pool["port"] = port
                                #     self.ip_data.append(ip)
            # run_pool = list(filter(lambda x: x not in exist_pool, self.ip_data))
            # 筛选设备
            run_pool = {}
            for run in self.ip_data:
                if run not in exist_pool:
                    run_pool[run] = self.ip_data.get(run)
            return run_pool
        else:
            self.ipPort_pool["port"] = self.ip_data.pop('port')
            run_pool = self.ip_data
            return run_pool


if __name__ == '__main__':
    # WifiConnect().connect_syc()
    a = WifiConnect()
    # print(a._ip())
    # print(a.ipPort_pool)
    lal = {'201bd2fd7d74': '192.168.10.140:5557', 'port': 5561}
    a.save_ip(lal)
    # a = read(PATH("../data/ip.pickle"))
