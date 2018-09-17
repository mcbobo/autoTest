import unittest
from datetime import datetime

from common.BaseRunner import ParametrizedTestCase
from common.BaseStatistics import countDate
from test_case.test_case.test_login_new import TestLogin
from test_case.HomeTest import HomeTest


class CaseManager:
    def __init__(self, devices):
        self.devices = devices

    def _suite(self):
        suite = unittest.TestSuite()
        suite.addTest(ParametrizedTestCase.parametrize(HomeTest, param=self.devices))
        # suite.addTest(ParametrizedTestCase.parametrize(TestLogin, param=self.devices))  # 加入测试类
        return suite

    def runner_case_app(self):
        start_time = datetime.now()
        suite = self._suite()
        unittest.TextTestRunner(verbosity=2).run(suite)
        end_time = datetime.now()
        countDate(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str((end_time - start_time).seconds) + "秒")
