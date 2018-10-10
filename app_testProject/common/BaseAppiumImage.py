# coding:utf-8
import os
import tempfile
import aircv as ac
import cv2
# import pytesseract
import time
from common.BaseImage import image_to_str
import selenium.common.exceptions

# from selenium.common.exceptions import NoSuchElementException

TPATH = lambda p: os.path.abspath(p)
TEMP_FILE = TPATH(tempfile.gettempdir() + "/temp_screen.png")


# def set_imageSize(func):
#     def wapper(self, imobj, imsrc=None):
#         self.driver.get_screenshot_as_file(TEMP_FILE)
#         if self.get_window_size().get('height') == 500:
#             imsrc = ac.imread(TEMP_FILE)
#             return func(imobj, imsrc)
#         else:
#             img = Image.open(TEMP_FILE)
#             img.thumbnail((900, 500), Image.ANTIALIAS)
#             img.save(TEMP_FILE, 'png')
#             imsrc = ac.imread(TEMP_FILE)
#             return func(imobj, imsrc)
#
#     return wapper


class AppiumImage:
    position = {}

    def __init__(self, driver):
        self.driver = driver

    def get_window_size(self):
        return self.driver.get_window_size()

    def swipe(self, start_x, start_y, end_x, end_y, duration):
        return self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    # @set_imageSize
    def find_element_by_image(self, img_path):
        # 根据路径图片得到设备上的坐标,resolution为设备的分辨率字典比例（分辨率默认为900x500）
        flag = 0
        imobj = cv2.imread(img_path)
        resolution = {1920: 2.13, 1280: 1.42, 1812: 2.013, 900: 1, 1794: 1.993}
        width, height = [self.get_window_size()[k] for k in ('width', 'height')]
        longest = width if width > height else height
        while flag < 3:
            self.driver.get_screenshot_as_file(TEMP_FILE)
            imsrc = cv2.imread(TEMP_FILE)
            if longest != 900:
                if width > height:
                    imsrc = cv2.resize(imsrc, (900, 500))
                else:
                    imsrc = cv2.resize(imsrc, (500, 900))
            try:
                pos = ac.find_template(imsrc, imobj, 0.7).get('result')
            except AttributeError:
                flag += 1
                time.sleep(3)
            else:
                return [tuple([i * resolution[longest] for i in pos])]
        raise selenium.common.exceptions.NoSuchElementException('can not find element')

    # @staticmethod
    def element_position(self, img):
        if AppiumImage.position.get(img):
            return AppiumImage.position[img]
        else:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            img_path = os.path.join(base_dir, 'data', 'element', img)
            p = self.find_element_by_image(img_path)
            AppiumImage.position[img] = p
            return AppiumImage.position[img]

    def _room_id_image(self):
        # 自定义截取范围，得到一个大概的房间id位置的图片（智萌德州房间id，写死了截取范围）
        self.driver.get_screenshot_as_file(TEMP_FILE)
        image = cv2.imread(TEMP_FILE)
        # p = r'D:\room.png'
        # image = cv2.imread(p)
        # image = Image.open(p)
        # (x, y) = image.size
        # x1, x2, y1, y2 = x * 0.14, x * 0.21, y * 0.03, y * 0.09
        x, y = image.shape[:2]
        return image[int(x * 0.02):int(x * 0.08), int(y * 0.166):int(y * 0.234)]

    def room_id(self):
        # 识别图中数字并提取
        room_id_img = self._room_id_image()
        # img = image_processing(room_id_img)
        # room_num = pytesseract.image_to_string(img, lang="eng", config="-psm 7")
        # code = code.encode('utf-8')
        # num = filter(str.isdigit, code)
        # num = room_num.strip().split(' ')
        num = image_to_str(room_id_img).strip().split(' ')
        return num[0] if len(num[0]) > 2 else num[1]


if __name__ == '__main__':
    from common.desired_caps1 import appium_desired

    # path = r'../picture/loginBtn.png'
    path = r'D:\soft\pyc\auto_appium\app_testProject\data\element\pwd.png'
    driver = appium_desired()
    star_time = time.time()
    pos = AppiumImage(driver).element_position(path)
    driver.tap(pos)
    # p1 = r'D:\soft\pyc\auto_appium\app_testProject\data\element\num.png'
    # pos1 = AppiumImage(driver).element_position(p1)
    # driver.tap(pos1)
    # time.sleep(3)
    # pos = AppiumImage(driver).element_position(path)
    # driver.tap(pos)
    # end_time = time.time()
    # print('total time:%s' % (end_time - star_time))
    # img1 = r"D:\Hlddz\t1.png"
    # imsrc = cv2.imread(img1)
    # imobj = cv2.imread(path)
    # result = ac.find_template(imsrc, imobj, 0.7).get('result')
    # print(result)
