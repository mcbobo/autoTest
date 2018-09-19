# -*- coding:utf-8 -*-
import yaml
from yaml.scanner import ScannerError
import os


def getYam(path):
    try:
        with open(path, encoding='utf-8') as f:
            x = yaml.load(f)
            return [True, x]
    except FileNotFoundError:
        print("==用例文件不存在==")
        app = {'check': [{'element_info': '', 'operate_type': 'get_value', 'find_type': 'ids', 'info': '用例文件不存在'}],
               'testinfo': [{'title': '', 'id': '', 'info': '', "msg": ""}],
               'testcase': [{'element_info': '', 'info': '', 'operate_type': '', 'find_type': ''},
                            {'element_info': '', 'msg': "", 'operate_type': '', 'find_type': '', 'info': ''},
                            {'element_info': '', 'msg': '', 'operate_type': '', 'find_type': '', 'info': ''},
                            {'element_info': '', 'info': '', 'operate_type': '', 'find_type': ''}]}

        return [False, app]
    except yaml.scanner.ScannerError:
        app = {'check': [{'element_info': '', 'operate_type': 'get_value', 'find_type': 'ids', 'info': '用例文件格式错误'}],
               'testinfo': [{'title': '', 'id': '', 'info': '', "msg": " "}],
               'testcase': [{'element_info': '', 'info': '', 'operate_type': '', 'find_type': ''},
                            {'element_info': '', 'msg': "", 'operate_type': '', 'find_type': '', 'info': ''},
                            {'element_info': '', 'msg': '', 'operate_type': '', 'find_type': '', 'info': ''},
                            {'element_info': '', 'info': '', 'operate_type': '', 'find_type': ''}]}
        print("==用例格式错误==")
        return [False, app]


def getMultiYam(*args):
    # 传入路径给getMultiYam将多个用例yaml文件合成一个用例
    if len(args) > 1:
        case = {"testcase": [], "check": [], "testinfo": [{'info': '', 'title': '', 'id': ''}]}
        flag = []
        for i in args:
            info = getYam(i)
            flag.append(info[0])
            case["testcase"].extend(info[1]["testcase"])
            case["check"].extend(info[1]["check"])
            case["testinfo"][0]["title"] += info[1]["testinfo"][0]["title"] + '\n'
            case["testinfo"][0]["info"] += info[1]["testinfo"][0]["info"] + '\n'
            case["testinfo"][0]["id"] += info[1]["testinfo"][0]["id"] + '\n'
        return [all(flag), case]
    else:
        return getYam(args[0])


if __name__ == '__main__':
    import os

    PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    # print(PATH("../yaml/home/firstOpen.yaml"))
    t1 = r'D:\soft\pyc\test\auto_appium\app_testProject\yamls\home\firstOpen.yaml'
    t2 = r'D:\soft\pyc\test\auto_appium\app_testProject\yamls\home\login.yaml'
    # print(getMultiYam(PATH("../yamls/home/firstOpen.yaml")))
    testinfo = getMultiYam(t1)[1]["testinfo"]
    print(testinfo)
    testinfo[0]["msg"] = 'test'
    print(testinfo)

    # port = str(random.randint(4700, 4900))
    # bpport = str(random.randint(4700, 4900))
    # devices = "DU2TAN15AJ049163"
    #
    # cmd1 = "appium --session-override  -p %s -bp %s -U %s" % (port, bpport, devices)
    # print(cmd1)
    # os.popen(cmd1)
