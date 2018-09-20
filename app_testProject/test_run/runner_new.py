# -*- coding: utf-8 -*-
import sys

sys.path.append("..")
import platform
from common.BaseAndroidPhone import *
from common.BaseAdb import *
from common.BaseAppiumServer import AppiumServer
from multiprocessing import Pool
from common.BaseInit import init, mk_file
from common.BaseStatistics import countDate, writeExcel, countSumDevices
from common.BasePickle import *
from datetime import datetime
from common.BaseApk import ApkInfo
from common.devices import devices
from test_case.case_manager import CaseManager
from common.BaseEmail import *

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def kill_adb():
    if platform.system() == "Windows":
        # os.popen("taskkill /f /im adb.exe")
        os.system(PATH("../app/kill5037.bat"))
    else:
        os.popen("killall adb")
    os.system("adb start-server")


def runnerPool(getDevices):
    devices_Pool = []

    for i in range(0, len(getDevices)):
        _pool = []
        _initApp = {}
        _initApp["deviceName"] = getDevices[i]["deviceName"]
        _initApp["platformVersion"] = getDevices[i]["platformVersion"]
        _initApp["platformName"] = "android"
        _initApp["port"] = getDevices[i]["port"]
        # _initApp["automationName"] = "uiautomator2"
        _initApp["systemPort"] = getDevices[i]["systemPort"]

        _initApp["app"] = getDevices[i]["app"]
        # apkInfo = ApkInfo(_initApp["app"])
        _initApp["appPackage"] = getDevices[i]["appPackage"]
        _initApp["appActivity"] = getDevices[i]["appActivity"]
        _pool.append(_initApp)
        devices_Pool.append(_initApp)

    pool = Pool(len(devices_Pool))
    pool.map(runnerCaseApp, devices_Pool)
    pool.close()
    pool.join()


def runnerCaseApp(devices):
    # starttime = datetime.now()
    # suite = unittest.TestSuite()
    # suite.addTest(ParametrizedTestCase.parametrize(HomeTest, param=devices))
    # # suite.addTest(ParametrizedTestCase.parametrize(HomeTest, param=devices)) #加入测试类
    # unittest.TextTestRunner(verbosity=2).run(suite)
    # endtime = datetime.now()
    # countDate(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str((endtime - starttime).seconds) + "秒")
    return CaseManager(devices).runner_case_app()


if __name__ == '__main__':
    app_path = {"app": r'D:\dr.fone3.2.0.apk'}
    devicess = devices()
    if not devices():
        kill_adb()
        devicess = devices()
    length = len(devicess)
    if length > 0:
        mk_file(**devicess[0])
        # # l_devices = []
        # # for dev in devicess:
        # #     app = {}
        # #     app["devices"] = dev
        # #     init(dev)
        # #     app["port"] = str(random.randint(4700, 4900))
        # #     app["bport"] = str(random.randint(4700, 4900))
        # #     app["systemPort"] = str(random.randint(4700, 4900))
        # #     app["app"] = PATH("../app/com.ximalaya.ting.android.apk")  # 测试的app路径,喜马拉雅app
        # #
        # #     l_devices.append(app)
        #
        appium_server = AppiumServer(devicess)
        appium_server.start_server()
        runnerPool(devicess)
        writeExcel()
        appium_server.stop_server(devicess)

        # 发送测试报告
        # text = latest_log(length)
        # att_path = latest_report()
        # user = get_csv_data(1)
        # send_mail(user[0], user[1], user[2], text, att_path)
    else:
        print("没有可用的安卓设备")
