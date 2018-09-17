from devices import udid
from multi_appiuim import appium_start
from check_port import check_port, release_port
from common.desired_caps import appium_desired
from time import sleep
import multiprocessing


def start_appium_action(host, port):
    if check_port(host, port):
        appium_start(host, port)
        # sleep(2)
        # return True
        return False
    else:
        print('appium %s start fail' % port)
        # return False
        return True


def start_devices_action(udid, port):
    host = '127.0.0.1'
    if start_appium_action(host, port):
        appium_desired(udid, port)
    else:
        release_port(port)


def appium_start_sync():
    print('=====appium_start_sync=====')

    appium_process = []

    for i in range(2):
        host = '127.0.0.1'
        port = 4723 + 2 * i

        appium = multiprocessing.Process(target=start_appium_action, args=(host, port))
        appium_process.append(appium)

    for appium in appium_process:
        appium.start()
    for appium in appium_process:
        appium.join()


def devices_star_sync():
    print('======devices_star_sync===')

    desired_process = []
    devices_list = udid()

    for i in range(len(devices_list)):
        port = 4723 + 2 * i
        desired = multiprocessing.Process(target=start_devices_action, args=(devices_list[i], port))
        desired_process.append(desired)

    for desired in desired_process:
        desired.start()
    for desired in desired_process:
        desired.join()


if __name__ == '__main__':
    # appium_start_sync()
    devices_star_sync()
