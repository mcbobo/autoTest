# coding:utf-8
import os
import socket
import multiprocessing
from multiprocessing import Process
import subprocess
import platform
import time

from common.BasePickle import read, write
from common.BaseAppiumServer import RunServer

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
        # self.lock = multiprocessing.Lock()

    # 多线程无线连接设备
    def connect_syc(self):
        run_pool = self._ip()
        num = len(run_pool) if len(run_pool) < 5 else 5

        if num > 0:
            print('连接前：%s' % self.ip_data)
            print('连接前ipPort:%s' % self.ipPort_pool)
            pool = multiprocessing.Pool(processes=num)
            run_list = list(run_pool.values())

            pool.map(self.connect, run_list)
            print('连接后：%s' % self.ip_data)
            print('连接后ipPort:%s' % self.ipPort_pool)
            #     self.ip_data.update(self.ipPort_pool)
            #     # self.save_ip(self.ip_data)
            # elif len(self.ipPort_pool) > 0 and num == 0:
            #     self.ip_data.update(self.ipPort_pool)
            #     self.save_ip(self.ip_data)
            #     print('saved')
            # else:
            #     print("no android device needs connect")
        print('pool:%s' % self.pool)

    # adb无线连接设备
    def connect(self, ip_port):
        temp = ip_port.split(':')
        port = temp[-1]
        ip = temp[0]
        cmd1 = "adb tcpip " + str(port)
        cmd2 = "adb connect " + ip_port

        if self.check_port(ip, int(port)):
            os.popen(cmd1)
        status = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).stdout.readlines()
        if status[0].decode().find("connected") >= 0:
            print("connected to %s" % ip_port)
        else:
            print("unable to connect to %s" % ip_port)
            self._remove(ip_port)
            print("del:%s" % self.ip_data)

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
        print("start saving")
        write(data, PATH("../data/ip.pickle"))

    def _remove(self, data):
        print('remove')
        for k, v in self.ip_data.items():
            if v == data:
                print('delete %s' % self.ip_data.pop(k))
                break

    def _ip(self):
        """
        获取设备ip地址
        :return: run_pool
        """
        cmd = 'adb devices'
        ip_str = 'inet addr:'
        dev = os.popen(cmd).readlines()
        len_devices = len(dev) - 1
        port = self.ip_data.pop("port", 5555)
        self.ipPort_pool['port'] = port

        if len_devices > 1:
            for d in range(1, len_devices):
                uid = dev[d].split('\t')[0]
                if self.ip_data.get(uid):
                    self.ipPort_pool[uid] = self.ip_data.pop(uid)
                    print("local saved the equipment：%s" % uid)
                elif uid in self.ip_data.values():
                    # 已连接的无线设备，删掉ip_data的键值对
                    print('connected device：%s' % uid)
                    for key, value in self.ip_data.items():
                        if uid == value:
                            self.ipPort_pool[key] = self.ip_data.pop(key)
                            break
                elif uid.find('.') >= 0:
                    pass
                else:
                    # 新的设备
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
                            # run_pool = list(filter(lambda x: x not in exist_pool, self.ip_data))
                            # 筛选设备
                            # run_pool = {}
                            # for run in self.ip_data:
                            #     if run not in self.ipPort_pool:
                            #         run_pool[run] = self.ip_data.get(run)
                            # return run_pool
                            # else:
                            # if len(self.ip_data) > 1:
                            # self.ipPort_pool["port"] = self.ip_data.pop('port')
                            # run_pool = self.ip_data
        self.ipPort_pool["port"] = port
        return self.ip_data

    def con_sync(self, run_list):
        """
        wifi connect
        """
        # run_pool = self._ip()
        # run_list = list(self._ip().values())

        for ip_port in run_list:
            print('start_time:%s' % time.time())
            temp = ip_port.split(':')
            port = temp[-1]
            ip = temp[0]
            cmd1 = "adb tcpip " + str(port)
            cmd2 = "adb connect " + ip_port

            if self.check_port(ip, int(port)):
                subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
            if platform.system() == "Windows":  # windows下启动server
                t1 = RunServer(cmd2)
                p = Process(target=t1.start())
                p.start()

                while True:
                    print("--------start_connect-------------")
                    if self.device_is_connect(ip_port):
                        print("-------win_connect_ 成功--------------")
                        break
                    else:
                        print("fail")
                        break
            else:
                status = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
                                          close_fds=True)
                while True:
                    info_line = status.stdout.readline().strip().decode()
                    time.sleep(1)
                    print("---------start_server----------")
                    if "connected" in info_line:
                        print("connected to %s" % ip_port)
                    else:
                        print("unable to connect to %s" % ip_port)
                        self._remove(ip_port)
                        print("del:%s" % self.ip_data)

    @staticmethod
    def device_is_connect(ip_port):
        cmd = "adb devices"
        dev_line = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
        # print(dev_line)
        len_devices = len(dev_line) - 1
        if len_devices > 1:
            for d in range(1, len_devices):
                uid = dev_line[d].decode().split('\t')[0]
                if uid == ip_port:
                    print("connected to %s" % ip_port)
                    return True
            else:
                print("unable to connect to %s" % ip_port)
                return False


if __name__ == '__main__':
    # a = WifiConnect()
    l = ['192.168.10.140:5557', '192.168.10.18:5559']
    WifiConnect().con_sync(l)
    # a = WifiConnect()
    # print('run:%s' % a._ip())
    # print('new:%s' % a.ipPort_pool)
    # print('ip_data:%s' % a.ip_data)
    # lal = {'201bd2fd7d74': '192.168.10.140:5557', 'port': 5561, 'HMKNW17A14019270': '192.168.10.18:5559'}
    # lal={}
    # a.save_ip(lal)
    # a = read(PATH("../data/ip.pickle"))
    # a.device_is_connect()
