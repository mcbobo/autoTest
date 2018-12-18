import os
import sys
import unittest
from common.BaseSetupDown_new import UpDown

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


# class HomeTest(ParametrizedTestCase):
class HomeTest(UpDown):
    # @unittest.skip('testFirstOpen')
    def testStatus(self):
        print("testStatus")
        casename = sys._getframe().f_code.co_name
        p1 = PATH('../yamls/home/t1.yaml')
        # p2 = PATH('../yamls/home/t2.yaml')
        self.template(casename, p1)

    @unittest.skip('login')
    def testLogining(self):
        casename = sys._getframe().f_code.co_name
        path = PATH('../yamls/home/t1.yaml')
        self.template(casename, path)

    # def testReceive(self):
    #     casename = sys._getframe().f_code.co_name
    #     path = PATH('../yamls/receive.yaml')
    #     self.template(casename, path)
    @unittest.skip('img')
    def testSendImg(self):
        casename = sys._getframe().f_code.co_name
        p1 = PATH('../yamls/sendImg.yaml')
        p2 = PATH('../yamls/receive_img.yaml')
        self.template(casename, p1)
        self.template(casename, p2)

    @unittest.skip('all')
    def testLogin(self):
        test_dir = PATH('../yamls/home')
        self.allCase(test_dir)
