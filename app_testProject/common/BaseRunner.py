# -*- coding: utf-8 -*-
import unittest
from appium import webdriver
import os
import time
import platform

from common.BaseLog import myLog
from common.BaseAdb import AndroidDebugBridge
from common.BaseElementEnmu import Element
from common.BaseAppiumServer import AppiumServer
from common.BaseYaml import getYam
from common.BasePickle import write

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def appium_testcase(devices):
    desired_caps = {}

    if str(devices["platformName"]).lower() == "android":
        # desired_caps['appPackage'] = devices["appPackage"]
        # desired_caps['appActivity'] = devices["appActivity"]
        desired_caps['udid'] = devices["deviceName"]
        desired_caps['app'] = devices["app"]
        desired_caps['appPackage'] = devices["appPackage"]
        desired_caps['appActivity'] = devices["appActivity"]
        # desired_caps["recreateChromeDriverSessions"] = "True"
        # 解决多次切换到webview报错问题，每次切换到非chrome-Driver时kill掉session 注意这个设置在appium 1.5版本上才做了处理
    else:
        # desired_caps['automationName'] = devices["automationName"] # Xcode8.2以上无UIAutomation,需使用XCUITest
        desired_caps['bundleId'] = devices["bundleId"]
        desired_caps['udid'] = devices["udid"]
        # desired_caps['newCommandTimeout'] = 3600  # 1 hour

    desired_caps['platformVersion'] = devices["platformVersion"]
    desired_caps['platformName'] = devices["platformName"]
    # desired_caps["automationName"] = devices['automationName']
    desired_caps['deviceName'] = devices["deviceName"]
    desired_caps["noReset"] = "True"
    desired_caps['noSign'] = "True"
    desired_caps["unicodeKeyboard"] = "True"
    desired_caps["resetKeyboard"] = "True"
    desired_caps["systemPort"] = devices["systemPort"]

    # desired_caps['app'] = devices["app"]
    remote = "http://127.0.0.1:" + str(devices["port"]) + "/wd/hub"
    # remote = "http://127.0.0.1:" + "4723" + "/wd/hub"
    driver = webdriver.Remote(remote, desired_caps)

    # 判断屏幕是否亮屏，锁屏则按设备电源键
    if AndroidDebugBridge.is_screen_on(devices["deviceName"]):
        driver.keyevent(26)
    return driver


class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should  
        inherit from this class.  
    """

    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        global devicess
        devicess = param

    @classmethod
    def setUpClass(cls):
        pass
        cls.driver = appium_testcase(devicess)
        cls.devicesName = devicess["deviceName"]
        cls.logTest = myLog().getLog(cls.devicesName)  # 每个设备实例化一个日志记录器

    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.close_app()
        cls.driver.quit()
        pass

    def tearDown(self):
        pass

    @staticmethod
    def parametrize(testcase_klass, param=None):
        # print("---parametrize-----")
        # print(param)
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite


if __name__ == '__main__':
    from common.devices import devices

    ga = devices()
    # print(devices())
    appium_testcase(ga[0])
