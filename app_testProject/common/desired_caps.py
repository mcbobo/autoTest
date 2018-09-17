from appium import webdriver
import yaml
import logging
import logging.config
import os
from businessView.loginView import LoginView

CON_LOG = '../config/log.conf'
logging.config.fileConfig(CON_LOG)
logging = logging.getLogger()


def appium_desired(udid, port=4723):
    with open('../config/app_caps.yaml', 'r', encoding='utf-8') as file:
        data = yaml.load(file)

    desired_caps = {}
    desired_caps['platformName'] = data['platformName']
    desired_caps['platformVersion'] = data['platformVersion']
    desired_caps['deviceName'] = data['deviceName']
    desired_caps['udid'] = udid

    base_dir = os.path.dirname(os.path.dirname(__file__))
    app_path = os.path.join(base_dir, 'app', data['appname'])
    desired_caps['app'] = app_path

    desired_caps['appPackage'] = data['appPackage']
    desired_caps['appActivity'] = data['appActivity']
    desired_caps['noReset'] = data['noReset']

    logging.info('appium port:%s start run %s' % (port, udid))
    desired_caps['unicodeKeyboard'] = data['unicodeKeyboard']
    desired_caps['resetKeyboard'] = data['resetKeyboard']
    # toast location setting
    # desired_caps['automationName'] = 'uiautomator2'

    logging.info('start app...')
    driver = webdriver.Remote('http://' + str(data['ip']) + ':' + str(port) + '/wd/hub', desired_caps)
    driver.implicitly_wait(8)
    l = LoginView(driver)
    l.login_action('13545', 'zmjj')
    return driver


if __name__ == '__main__':
    # appium_desired('127.0.0.1:21513')
    PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    print(PATH('app'))
    # with open('../config/app_caps.yaml', 'r', encoding='utf-8') as file:
    #     data = yaml.load(file)
    #     print(type(data['udid'][1]))
    # base_dir=os.path.dirname(os.path.dirname(__file__))
    # print(os.path.dirname(__file__))
    # print(base_dir)
    #
    # app_path=os.path.join(base_dir,'app',data['appname'])
    # print(app_path)
