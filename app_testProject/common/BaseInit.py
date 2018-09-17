from common.BaseElementEnmu import Element
from common.BasePickle import *
from common.BaseFile import *
import logging

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def mk_file():
    destroy()
    mkdir_file(PATH("../Log/" + Element.INFO_FILE))
    mkdir_file(PATH("../Log/" + Element.SUM_FILE))
    mkdir_file(PATH("../Log/" + Element.DEVICES_FILE))

    data = read(PATH("../Log/" + Element.INFO_FILE))
    # data["appName"] = apkInfo.getApkName()
    # data["appSize"] = apkInfo.getApkSize()
    # data["appVersion"] = apkInfo.getApkBaseInfo()[2]
    data["versionCode"] = "40"
    data["versionName"] = "1.4.0"
    data["packingTime"] = "2017/12/4 13:00"
    data["sum"] = 0
    data["pass"] = 0
    data["fail"] = 0
    write(data=data, path=PATH("../Log/" + Element.SUM_FILE))


def init(devices):
    # 每次都重新安装uiautomator2都两个应用
    os.popen("adb -s %s uninstall io.appium.uiautomator2.server.test" % devices)
    os.popen("adb -s %s uninstall io.appium.uiautomator2.server" % devices)
    os.popen("adb -s %s install -r %s" % (devices, PATH("../app/appium-uiautomator2-server-v0.1.9.apk")))
    os.popen("adb -s %s install -r %s" % (devices, PATH("../app/appium-uiautomator2-server-debug-androidTest.apk")))
    # os.popen("adb install -r "+PATH("../app/android-system-webview-60.apk"))

    # 检查是否已安装settings、unlock两个应用,已经安装两个应用返回一个长度为4的列表
    status = os.popen("adb -s %s shell pm list packages io.appium." % devices).readlines()
    if len(status) != 4:
        logging.info('========install settings and unlock=========')
        os.popen("adb -s %s install -r %s" % (devices, PATH("../app/settings_apk-debug.apk")))
        os.popen("adb -s %s install -r %s" % (devices, PATH("../app/unlock_apk-debug.apk")))


def destroy():
    remove_file(PATH("../Log/" + Element.INFO_FILE))
    remove_file(PATH("../Log/" + Element.SUM_FILE))
    remove_file(PATH("../Log/" + Element.DEVICES_FILE))


if __name__ == '__main__':
    # print(destroy())
    app = os.popen("adb -s 127.0.0.1:21503 shell pm list packages io.appium.").readlines()
    # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    mk_file()
