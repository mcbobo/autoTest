# coding:utf-8
import logging
from common.common_fun import Common, NoSuchElementException, TimeoutException
# from common.desired_caps import appium_desired
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class LoginView(Common):
    # 登录前元素
    username_type = (By.ID, 'com.tencent.mm:id/hx')
    pwd_type = (By.ID, 'com.tencent.mm:id/cb_')
    password_type = (By.ID, 'com.tencent.mm:id/hx')
    loginBtn = (By.ID, 'com.tencent.mm:id/d1w')
    nextBtn = (By.ID, 'com.tencent.mm:id/ak_')
    tip_commit = (By.ID, 'com.tencent.mm:id/alk')
    failBtn = (By.ID, 'com.tencent.mm:id/kj')

    # 登录成功后元素
    button_mysefl = (By.ID, 'com.tencent.mm:id/c9d')
    personal_info = (By.ID, 'com.tencent.mm:id/ij')
    logoutBtn = (By.ID, 'com.tencent.mm:id/i8')
    logout_tip = (By.ID, 'com.tencent.mm:id/all')

    def check_login_fail(self):
        logging.info('=====check_login_fail====')
        try:
            self.driver.find_element(*self.failBtn)
        except NoSuchElementException:
            pass
        else:
            logging.error('login fail!')
            self.getScreenShot('login fail')
            return True

    def login_action(self, username, password, udid=''):

        logging.info('============login_action==============')
        logging.info('click loginBtn')
        self.driver.find_element(*self.loginBtn).click()

        logging.info('username is:%s' % username)
        # self.driver.find_element(*self.username_type).send_keys(username)
        username_element = self.driver.find_element(*self.username_type)
        self.fast_input(username_element, username, udid)
        # username_element.send_keys(username)
        self.driver.find_element(*self.nextBtn).click()
        if self.check_login_fail():
            return False

        logging.info('password is:%s' % password)
        password_element = WebDriverWait(self.driver, 5).until(lambda x: x.find_element(*self.password_type))
        # password_element.send_keys(password)
        self.fast_input(password_element, password, udid)
        self.driver.find_element(*self.nextBtn).click()
        if self.check_login_fail():
            return False

        self.check_account_alert()
        logging.info('login finished!')

    def check_account_alert(self):
        logging.info('=====check_account_alert====')
        try:
            element = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(*self.tip_commit))
            # element = self.driver.find_element(*self.tip_commit)
        except TimeoutException:
            logging.info('pass')
            pass
        else:
            logging.info('close tip_commit')
            element.click()

    def check_loginStatus(self):
        logging.info('====check_loginStatus======')
        try:
            element = WebDriverWait(self.driver, 10).until(lambda x: x.find_elements(*self.button_mysefl))
        except (NoSuchElementException, TimeoutException):
            logging.error('login fail!')
            self.getScreenShot('login fail')
            return False
        else:
            logging.info('login success!')
            element[3].click()
            self.logout_action()
            return True

    def logout_action(self):
        logging.info('=====logout_action======')
        self.driver.find_elements(*self.personal_info)[4].click()
        self.driver.find_elements(*self.personal_info)[10].click()
        self.driver.find_element(*self.logoutBtn).click()
        self.driver.find_element(*self.logout_tip).click()


if __name__ == '__main__':
    from test_run.runnerBase import appium_testcase
    from common.devices import devices

    driver = appium_testcase(devices()[0][0])
    l = LoginView(driver)
    # loc = (By.ID, 'com.tencent.mm:id/d1w')
    # loc = 'com.tencent.mm:id/d1w'
    # driver.find_element(value=loc).click()
    l.login_action('13726221317', 'zmjj123456')
    # l.check_loginStatus()
