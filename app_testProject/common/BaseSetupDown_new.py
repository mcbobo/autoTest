# coding:utf-8
import sys
import os

from common.BaseYaml import getMultiYam, getYam
from common.BaseRunner import ParametrizedTestCase as pt
from PageObject.Home.FirstOpenPage import FirstOpenPage


class UpDown(pt):
    @classmethod
    def setUpClass(cls):
        super(UpDown, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(UpDown, cls).tearDownClass()

    def template(self, case_name, *args):
        # 用例模板，参数化
        data = getMultiYam(*args)
        app = {"logTest": self.logTest, "driver": self.driver, "data": data,
               "device": self.devicesName, "caseName": case_name}

        page = FirstOpenPage(app)
        page.operate()
        page.checkPoint()

    def allCase(self, rootdir):
        # 遍历文件夹所有文件，run全部用例
        casename = sys._getframe().f_code.co_name
        files_path = []

        for rt, dirs, fileNames in os.walk(rootdir):
            files = os.listdir(rt)
            files = filter(lambda x: x if x in fileNames else None, files)
            files_path.extend([os.path.join(rt, i) for i in files])

        for path in files_path:
            self.template(casename, path)
