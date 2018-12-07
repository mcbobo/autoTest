from appium import webdriver
import yaml
import logging
import logging.config
import os
import time

CON_LOG = '../config/log.conf'
logging.config.fileConfig(CON_LOG)


# logging = logging.getdatager()


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

    driver.keyevent(26)
    time.sleep(3)
    print('start_up')
    driver.keyevent(26)
    return driver


def is_screen_on(device=''):
    if device == '':
        cmd = 'adb shell dumpsys window policy'
    else:
        cmd = 'adb -s ' + device + ' shell dumpsys window policy'
    screen_awake_value = '    mAwake=true\n'
    all_list = os.popen(cmd).readlines()
    if screen_awake_value in all_list:
        return True
    else:
        return False


if __name__ == '__main__':
    # appium_desired()
    print(is_screen_on())
