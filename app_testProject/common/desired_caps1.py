from appium import webdriver
import yaml
import logging
import logging.config
import os

CON_LOG = '../config/log.conf'
logging.config.fileConfig(CON_LOG)
logging = logging.getLogger()


def appium_desired():
    with open('../config/app_caps.yaml', 'r', encoding='utf-8') as file:
        data = yaml.load(file)

    desired_caps = {}
    desired_caps['platformName'] = data['platformName']
    desired_caps['platformVersion'] = data['platformVersion']
    desired_caps['deviceName'] = data['deviceName']

    base_dir = os.path.dirname(os.path.dirname(__file__))
    app_path = os.path.join(base_dir, 'app', data['appname'])
    desired_caps['app'] = app_path

    desired_caps['appPackage'] = data['appPackage']
    desired_caps['appActivity'] = data['appActivity']
    desired_caps['noReset'] = data['noReset']

    desired_caps['unicodeKeyboard'] = data['unicodeKeyboard']
    desired_caps['resetKeyboard'] = data['resetKeyboard']
    # toast location setting
    # desired_caps['automationName'] = 'uiautomator2'

    logging.info('start app...')
    driver = webdriver.Remote('http://' + str(data['ip']) + ':' + str(data['port']) + '/wd/hub', desired_caps)
    driver.implicitly_wait(8)
    return driver


if __name__ == '__main__':
    from common.BasePickle import *
    from common.BaseElementEnmu import Element

    PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    _read = readInfo(PATH("../Log/" + Element.INFO_FILE))
    # devices = '127.0.0.1:21513'
    # result = 0
    # if _read:
    #     for item in _read:
    #         if item["device"] == devices:  # 本地已经存在该设备记录
    #             if result:
    #                 item["pass"] = item["pass"] + 1
    #             else:
    #                 item["fail"] = item["fail"] + 1
    # print(_read)
