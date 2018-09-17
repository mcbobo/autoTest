import os
import sys
import unittest
from common.BaseRunner import ParametrizedTestCase
from PageObject.Home.FirstOpenPage import FirstOpenPage
from common.BaseYaml import getMultiYam
from common.BaseSetupDown_new import UpDown

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), p)
)


# class HomeTest(ParametrizedTestCase):
class TestLogin(UpDown):
    @unittest.skip('testFirstOpen')
    def testFirstOpen(self):
        # app = {"logTest": self.logTest, "driver": self.driver, "path": PATH("../yamls/home/firstOpen.yaml"),
        #        "device": self.devicesName, "caseName": sys._getframe().f_code.co_name}
        data = getMultiYam(PATH("../yamls/home/firstOpen.yaml"))
        app = {"logTest": self.logTest, "driver": self.driver, "data": data,
               "device": self.devicesName, "caseName": 'test_open'}

        page = FirstOpenPage(app)
        page.operate()
        page.checkPoint()

    def testLogin(self):
        casename = sys._getframe().f_code.co_name
        test_dir = PATH('../yamls/home')
        files = os.listdir(test_dir)
        files_path = [os.path.join(test_dir, i) for i in files]
        for path in files_path:
            self.template(casename, path)
