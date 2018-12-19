# -*- coding:utf-8 -*-
import yaml
from yaml.scanner import ScannerError


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
            if i == args[-1]:
                case["check"].extend(info[1]["check"])
            else:
                info[1]["check"][0]['case_check'] = 1
                case["testcase"].extend(info[1]["check"])
            case["testinfo"][0]["title"] += info[1]["testinfo"][0]["title"] + '_'
            case["testinfo"][0]["info"] += info[1]["testinfo"][0]["info"] + '_'
            case["testinfo"][0]["id"] += info[1]["testinfo"][0]["id"] + '_'
        return [all(flag), case]
    else:
        return getYam(args[0])


if __name__ == '__main__':
    import os

    from test_case.case_manager import Path

    PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    # print(PATH("../yaml/home/firstOpen.yaml"))
    t1 = PATH('../yamls/module.yaml')
    t2 = PATH('../yamls/home/t2.yaml')
    testinfo = getMultiYam(t1)
    print(testinfo[1])
    suitList = testinfo[1]
    for suitName in suitList:
        for caseName in suitList[suitName]:
            case = dict()
            pathList = list()
            for path in suitList[suitName][caseName]:
                casePath = '../yamls/' + str(suitName) + '/' + path
                pathList.append(casePath)
            # print(Path(pathList))
            case[caseName] = Path(pathList).path
            for i in case[caseName]:
                print(i)
            print(case)

# port = str(random.randint(4700, 4900))
# bpport = str(random.randint(4700, 4900))
# devices = "DU2TAN15AJ049163"
#
# cmd1 = "appium --session-override  -p %s -bp %s -U %s" % (port, bpport, devices)
# print(cmd1)
# os.popen(cmd1)
