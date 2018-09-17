import re
from math import floor
import subprocess
import os
import zipfile
import json

'''
apk文件的读取信息
'''


class ApkInfo():
    def __init__(self, apkPath):
        self.apkPath = apkPath

    # 得到app的文件大小
    def getApkSize(self):
        size = floor(os.path.getsize(self.apkPath) / (1024 * 1000))
        return str(size) + "M"

    def getApkBaseInfo(self):
        p = subprocess.Popen("aapt dump badging %s" % self.apkPath, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        match = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output.decode())
        if not match:
            raise Exception("can't get packageinfo")
        packageName = match.group(1)  # 包名
        versionCode = match.group(2)  # 版本号
        versionName = match.group(3)  # 版本名称

        print('packagename:' + packageName)
        print('versionCode:' + versionCode)
        print('versionName:' + versionName)
        return packageName, versionName, versionCode

    # 得到应用名字
    def getApkName(self):
        p = subprocess.Popen("aapt dump badging %s" % self.apkPath, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        t = output.decode().split()
        for item in t:
            # print(item)
            match = re.compile("application-label:(\S+)").search(item)
            if match is not None:
                return eval(match.group(1))

    # 得到启动类
    def getApkActivity(self):
        p = subprocess.Popen("aapt dump badging %s" % self.apkPath, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        print("=====getApkActivity=========")
        match = re.compile("launchable-activity: name=(\S+)").search(output.decode())
        print("match=%s" % match)
        if match is not None:
            return match.group(1)

    def get_app_icon(self):
        cmd = "aapt dump badging %s | findstr application-icon-120" % self.apkPath
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, err) = p.communicate()

        print("=====getApkIcon=========")
        match = re.compile("application-icon-120:(\S+)").search(output.decode())
        z = zipfile.ZipFile(self.apkPath)
        if match is not None:
            return z.read(eval(match.group(1)))


if __name__ == '__main__':
    path = 'D:\\dr.fone3.2.0.apk'
    print(ApkInfo(path).get_app_icon())
    pass
    # ApkInfo(r"D:\app\appium\Img\Jianshu-2.3.1.apk").getApkActivity()
    # ApkInfo(r"D:\app\appium\Img\Jianshu-2.3.1.apk").getApkActivity()
    # # ApkInfo(r"D:\app\appium_study\Img\t.apk").get_apk_version()
    # # ApkInfo(r"D:\app\appium_study\Img\t.apk").get_apk_name()
    # ApkInfo(r"D:\app\appium_study\img\t.apk").get_apk_activity()
    # ApkInfo(r"D:\app\appium_study\Img\t.apk").get_apk_activity()
