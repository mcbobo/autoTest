# coding:utf-8
import os
import unittest
from datetime import datetime
from common.BaseRunner import ParametrizedTestCase
from common.BaseStatistics import countDate
from common.BaseSetupDown_new import UpDown
from common.BaseYaml import getYam

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class CaseManager:
    """
    加载yaml文件动态生成测试模块
    yaml文件格式：{module:[{caseName:casePath1,...]}} ----casePath只需要写文件名即可,casePath一个用字符串，大于1用列表
    详细看_suits
    """

    def __init__(self, devices):
        self.devices = devices

    def _suite(self):
        suitPath = PATH('../yamls/module.yaml')
        suitList = getYam(suitPath)[1]
        suite = unittest.TestSuite()

        for suitName in suitList:
            case = dict()
            for caseName in suitList[suitName]:
                pathList = list()
                for path in suitList[suitName][caseName]:
                    casePath = '../yamls/' + str(suitName) + '/' + path
                    pathList.append(casePath)
                case[caseName] = Path(pathList)
            CaseClass = type(suitName, (Module,), case)
            suite.addTest(ParametrizedTestCase.parametrize(CaseClass, param=self.devices))
        # suite.addTest(ParametrizedTestCase.parametrize(HomeTest, param=self.devices))  # 加入测试类
        return suite

    def runner_case_app(self):
        start_time = datetime.now()
        suite = self._suite()
        unittest.TextTestRunner(verbosity=2).run(suite)
        end_time = datetime.now()
        countDate(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str((end_time - start_time).seconds) + "秒")


class Path:
    def __init__(self, path):
        self.path = [PATH(i) for i in path]
        # self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))

    def __str__(self):
        return '%s' % self.path


class ModuleMetaclass(type):
    """
    创建模块类的时候，自动添加用例方法
    eg：testLogin = Path(path)
    """

    def __new__(cls, name, bases, attrs):
        if name == 'Module':
            return type.__new__(cls, name, bases, attrs)
        print('Found Module: %s' % name)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Path):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            print('caseMethod: %s' % k)
            attrs[k] = lambda self, value=attrs.pop(k).path: self.template(k, *value)
        return type.__new__(cls, name, bases, attrs)


class Module(UpDown, metaclass=ModuleMetaclass):
    pass


if __name__ == '__main__':
    pass
    # c = Login()
    # c.testLogin()
    # print(type(c))
