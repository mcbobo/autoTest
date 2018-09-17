# coding:utf-8
import os
# import yaml
import random
from common.BaseYaml import getYam

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def devices():
    """返回已连接设备的udid"""
    device_list = []
    data = getYam(PATH('../config/app_caps.yaml'))[1]
    # with open('../config/app_caps.yaml', 'r', encoding='utf-8') as file:
    #     data = yaml.load(file)

    cmd = 'adb devices'
    dev = os.popen(cmd).readlines()
    len_devices = len(dev) - 1
    for i in range(1, len_devices):
        devices_dict = dict()
        devices_dict.update(data)
        devices_dict['udid'] = dev[i].split('\t')[0]
        devices_dict['port'] = 4721 + 2 * i
        devices_dict['bport'] = devices_dict['port'] + 1
        devices_dict['deviceName'] = devices_dict['udid']
        devices_dict["systemPort"] = str(random.randint(4700, 4900))
        devices_dict["automationName"] = "uiautomator2"

        base_dir = os.path.dirname(os.path.dirname(__file__))
        app_path = os.path.join(base_dir, 'app', data['appname'])
        devices_dict['app'] = app_path
        # device_list.append([])
        # device_list[i - 1].append(devices_dict)
        device_list.append(devices_dict)
    return device_list


def udid():
    device_list = []

    cmd = 'adb devices'
    dev = os.popen(cmd).readlines()
    len_devices = len(dev) - 1
    for i in range(1, len_devices):
        device_list.append(dev[i].split('\t')[0])
    return device_list


if __name__ == '__main__':
    print(devices())
    # for i in devices():
    #     print(i)
