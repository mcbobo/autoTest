import os
import sys
import unittest
from PageObject.Home.FirstOpenPage import FirstOpenPage
from common.BaseYaml import getMultiYam
from common.BaseSetupDown_new import UpDown

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


# class HomeTest(ParametrizedTestCase):
class HomeTest(UpDown):
    # @unittest.skip('testFirstOpen')
    def testFirstOpen(self):
        casename = sys._getframe().f_code.co_name
        path = PATH('../yamls/home/firstOpen.yaml')
        self.template(casename, path)

    def testDevice(self):
        casename = sys._getframe().f_code.co_name
        path = PATH('../yamls/home/login.yaml')
        self.template(casename, path)

    @unittest.skip('all')
    def testLogin(self):
        test_dir = PATH('../yamls/home')
        self.allCase(test_dir)
