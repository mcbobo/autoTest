import xlsxwriter

# from Base.BaseAndroidPhone import getPhoneInfo
from common.BaseElementEnmu import Element
from common.BaseExcel import OperateReport
from common.BaseInit import destroy
from common.BasePickle import *
from datetime import datetime

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

'''
统计数据相关
'''

'''
result bool
logTest 记录日志类 class
driver
testinfo

'''


def countInfo(**kwargs):
    # get_phone = getPhoneInfo(kwargs["devices"])
    # phone_name = get_phone["brand"] + "_" + get_phone["model"] + "_" + "android" + "_" + get_phone["release"]
    _info = {}
    step = ""  # 操作步骤信息
    check_step = ""  # 检查点步骤信息

    for case in kwargs["testCase"]:
        step = step + case["info"] + "\n"

    if type(kwargs["testCheck"]) == list:  # 检查点为列表
        for check in kwargs["testCheck"]:
            check_step = check_step + check["info"] + "\n"
    elif type(kwargs["testCheck"]) == dict:
        check_step = kwargs["testCheck"]["info"]
    else:
        print("获取检查点步骤数据错误，请检查")
        print(kwargs["testCheck"])

    _info["step"] = step  # 用例操作步骤
    _info["checkStep"] = check_step  # 用例检查点

    if kwargs["result"]:
        _info["result"] = "通过"
        kwargs["logTest"].checkPointOK(driver=kwargs["driver"], caseName=kwargs["testInfo"][0]["title"],
                                       checkPoint=kwargs["caseName"] + "_" + kwargs["testInfo"][0].get(
                                           "msg", " "))
    else:
        _info["result"] = "失败"  # 用例接开关
        _info["img"] = kwargs["logTest"].checkPointNG(driver=kwargs["driver"], caseName=kwargs["testInfo"][0]["title"],
                                                      checkPoint=kwargs["caseName"] + "_" + kwargs["testInfo"][0].get(
                                                          "msg", " "))
    _info["id"] = kwargs["testInfo"][0]["id"]  # 用例id
    _info["title"] = kwargs["testInfo"][0]["title"]  # 用例名称
    _info["caseName"] = kwargs["caseName"]  # 测试函数
    _info["phoneName"] = kwargs["phoneName"]  # 手机名
    _info["msg"] = kwargs["testInfo"][0].get("msg", "")  # 备注
    _info["info"] = kwargs["testInfo"][0]["info"]  # 前置条件

    writeInfo(data=_info, path=PATH("../data/" + Element.INFO_FILE))
    # print(read(PATH("../data/info.pickle")))


# 本地没有设备用例的记录统计
def countSumNoDevices(devices, result, _read, phone_info):
    if _read is None:
        _read = []
    # get_phone = getPhoneInfo(devices)
    # phone_name = get_phone["brand"] + "_" + get_phone["model"] + "_" + "android" + "_" + get_phone["release"]
    app = {"phone_name": phone_info['phone_name'], "pass": 0, "fail": 0, "device": devices,
           "release": phone_info['release']}
    if result:
        app["pass"] = 1
    else:
        app["fail"] = 1
    _read.append(app)
    write(data=_read, path=PATH("../data/" + Element.DEVICES_FILE))
    print(read(PATH("../data/" + Element.DEVICES_FILE)))

    return


# 统计各个设备成功失败的用例数
def countSumDevices(devices, result, phone_info):
    _read = readInfo(PATH("../data/" + Element.DEVICES_FILE))
    if _read:
        for item in _read:
            if item["device"] == devices:  # 本地已经存在该设备记录
                if result:
                    item["pass"] = item["pass"] + 1
                else:
                    item["fail"] = item["fail"] + 1
                write(data=_read, path=PATH("../data/" + Element.DEVICES_FILE))
                return
    countSumNoDevices(devices, result, _read, phone_info=phone_info)
    print(read(PATH("../data/" + Element.DEVICES_FILE)))

    # else:
    #     print("------0------")
    #     countSumNoDevices(devices, result)
    #     print("---countSumDevices---")
    #     print(read(PATH("../data/" + Element.DEVICES_FILE)))


# 统计所有用例数
def countSum(result):
    # print("----countSum----")
    data = {"sum": 0, "pass": 0, "fail": 0}
    _read = read(PATH("../data/sum.pickle"))
    if _read:
        data = _read
    data["sum"] = data["sum"] + 1
    if result:
        data["pass"] = data["pass"] + 1
    else:
        data["fail"] = data["fail"] + 1
    write(data=data, path=PATH("../data/" + Element.SUM_FILE))
    # print(read(PATH("../data/sum.pickle")))


# def write_reconnect(msg, path=""):
#     write(msg, path=path)
#     # print(read_reconnect(path))

# 统计所有用例开始时间和消耗时间
def countDate(testDate, testSumDate):
    print("--------- countDate------")
    data = read(PATH("../data/" + Element.SUM_FILE))
    print(data)
    if data:
        data["testDate"] = testDate
        data["testSumDate"] = testSumDate
        write(data=data, path=PATH("../data/" + Element.SUM_FILE))
    else:
        print("统计数据失败")


'''
测试报告
'''


def writeExcel():
    workbook = xlsxwriter.Workbook(PATH('../Report/' + Element.REPORT_FILE))
    worksheet = workbook.add_worksheet("测试总况")
    worksheet2 = workbook.add_worksheet("测试详情")
    operateReport = OperateReport(workbook)
    operateReport.init(worksheet, read(PATH("../data/" + Element.SUM_FILE)),
                       read(PATH("../data/" + Element.DEVICES_FILE)))
    operateReport.detail(worksheet2, readInfo(PATH("../data/" + Element.INFO_FILE)))
    operateReport.close()

    # destroy()  # 删除文件


if __name__ == '__main__':
    # data = {'result': '失败', 'caseName': 'FirstOpenTest', 'title': '第一次打开', 'phoneName': 'samsung_GT-I9500_android_4.4.2', 'img': 'D:\\app\\appium\\log\\samsung_GT-I9500_android_4.4.220170607184558\\第一次打开CheckPoint_1_NG.png', 'id': 'test001'}
    # writeInfo(data, PATH("../data/info.pickle"))
    # writeInfo(data, PATH("../data/info.pickle"))
    # _read = readInfo(PATH("../data/info.pickle"))
    writeExcel()
