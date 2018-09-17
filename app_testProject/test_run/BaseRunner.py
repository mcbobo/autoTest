# -*- coding: utf-8 -*-
# from Base.BaseAppiumServer import AppiumServer
# from Base.BaseLog import myLog
import unittest
from appium import webdriver
import logging
import logging.config
import os
# from Base.BaseElementEnmu import Element
import platform
import time

# PATH = lambda p: os.path.abspath(
#     os.path.join(os.path.dirname(__file__), p)
# )
CON_LOG = '../config/log.conf'
logging.config.fileConfig(CON_LOG)
logging = logging.getLogger()


def appium_testcase(devices):
    desired_caps = {}

    if str(devices["platformName"]).lower() == "android":
        # desired_caps['appPackage'] = devices["appPackage"]
        # desired_caps['appActivity'] = devices["appActivity"]
        desired_caps['udid'] = devices["udid"]
        desired_caps['app'] = devices["app"]
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
    logging.info('appium port:%s start run %s' % (devices['port'], devices['udid']))

    desired_caps['app'] = devices["app"]
    remote = "http://127.0.0.1:" + str(devices["port"]) + "/wd/hub"
    # remote = "http://127.0.0.1:" + "4723" + "/wd/hub"
    logging.info('start app...')
    driver = webdriver.Remote(remote, desired_caps)
    return driver


class ParametrizedTestCase(unittest.TestCase):
    """ unittest参数化,TestCase classes that want to be parametrized should  
        inherit from this class.  
    """

    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        global devicess
        devicess = param

    @staticmethod
    def setUpClass():
        pass
        # cls.driver = appium_testcase(devicess)
        # cls.devicesName = devicess["deviceName"]
        # # cls.logTest = myLog().getLog(cls.devicesName)  # 每个设备实例化一个日志记录器

    def setUp(self):
        self.driver = appium_testcase(devicess)

    @staticmethod
    def tearDownClass():
        print('tearDownClass')

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

    # print(appium_testcase(devices()[0]))
    appium_testcase(devices()[1])
