# -*- coding: utf-8 -*-
import sys

sys.path.append("..")
import datetime
import time
import unittest
from multiprocessing import Pool
from runnerBase import TestInterfaceCase
from common.devices import devices
import logging
from test_case.test_login import TestLogin


# def get_devices():
#     return devices()


# ga = get_devices()


def runnerPool(devices_Pool):
    # devices_Pool = getDevices
    pool = Pool(len(devices_Pool))
    # for i in range(2):
    #     pool.apply_async(sample_request, args=(t[i],)) # 异步
    pool.map(runnerCaseApp, devices_Pool)
    pool.close()
    pool.join()


def runnerCaseApp(l_devices):
    start_test_time = time.strftime("%Y-%m-%d %H:%M %p", time.localtime())
    starttime = datetime.datetime.now()
    suite = unittest.TestSuite()
    suite.addTest(TestInterfaceCase.parametrize(TestLogin, l_devices=l_devices))
    unittest.TextTestRunner(verbosity=2).run(suite)
    endtime = datetime.datetime.now()
    logging.info('=====start at %s spend %s=====' % (start_test_time, endtime - starttime))
    # report()


if __name__ == '__main__':
    from common.BaseAppiumServer import AppiumServer

    ga = devices()
    # print(ga)
    # ser = AppiumServer(ga)
    # ser.start_server()
    runnerPool(ga)
