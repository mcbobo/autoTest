import logging
from common.common_fun import Common, NoSuchElementException, TimeoutException
from common.desired_caps import appium_desired
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from .loginView import LoginView


class MwgView(Common):
    # 搜索元素
    searchBtn = (By.ACCESSIBILITY_ID, '搜索')
    sendBtn = (By.ID, 'com.tencent.mm:id/hx')
    # 魅玩购元素
    content = u'运动领袖汇'
    mwg_enterBtn = (By.ID, 'com.tencent.mm:id/l7')
    mwg = (By.ID, 'com.tencent.mm:id/aaq')
    # 关注魅玩购元素
    mwg_view = ''
    search_mwg = (By.ID, 'com.tencent.mm:id/bb2')
    mwg_info = (By.ID, '')
    followMwg = (By.NAME, '关注')

    def open_mwg(self):
        logging.info('============open_mwg==============')
        self.type_weixin_search(self.searchBtn, self.searchBtn, self.content)
        try:
            element = WebDriverWait(self.driver, 5).until(lambda x: x.find_element(*self.mwg_enterBtn))
        except TimeoutException:
            logging.info('not follow mwg,start follow mwg')
            self.follow_mwg()
        else:
            logging.info('followed mwg,open mwg')
            element.click()
        self.find_element(*self.mwg).click()
        logging.info('open finished!')

    def follow_mwg(self):
        logging.info('============follow_mwg==============')
        self.find_element(*self.search_mwg).click()
        WebDriverWait(self.driver, 5).until(lambda x: x.find_element_by_class_name('android.webkit.WebView'))
        self.driver.switch_to.context(self.mwg_view)
        self.find_element(*self.mwg_info).click()
        self.driver.switch_to.context('NATIVE_APP')
        self.find_element(*self.followMwg).click()
        logging.info('follow finished')
