from common.BaseElementEnmu import Element
from common.BasePickle import *
from common.BaseFile import *
from common.BaseApk import ApkInfo

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def mk_file(**kwargs):
    destroy()
    mkdir_file(PATH("../Log/" + Element.INFO_FILE))
    mkdir_file(PATH("../Log/" + Element.SUM_FILE))
    mkdir_file(PATH("../Log/" + Element.DEVICES_FILE))

    data = read(PATH("../Log/" + Element.INFO_FILE))
    apk = ApkInfo(kwargs['app'])
    data["appName"] = apk.getApkName()
    data["icon"] = ApkInfo(kwargs['app']).get_app_icon()
    # data["appVersion"] = apkInfo.getApkBaseInfo()[2]
    info = apk.getApkBaseInfo()
    data["versionCode"] = info[2]
    data["versionName"] = info[1]
    data["packageName"] = info[0]
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
        print('========install settings and unlock=========')
        os.popen("adb -s %s install -r %s" % (devices, PATH("../app/settings_apk-debug.apk")))
        os.popen("adb -s %s install -r %s" % (devices, PATH("../app/unlock_apk-debug.apk")))


def destroy():
    remove_file(PATH("../Log/" + Element.INFO_FILE))
    remove_file(PATH("../Log/" + Element.SUM_FILE))
    remove_file(PATH("../Log/" + Element.DEVICES_FILE))


if __name__ == '__main__':
    # print(destroy())
    # app = os.popen("adb -s 127.0.0.1:21503 shell pm list packages io.appium.").readlines()
    # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    app_path = {"app": r'D:\dr.fone3.2.0.apk'}
    mk_file(**app_path)
