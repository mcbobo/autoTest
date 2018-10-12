# coding=utf-8
from PIL import Image
import pytesseract
import cv2
import time


def _gray_image(im):
    # 自适应阀值二值化
    # print('.....' + img_name)
    # im = cv2.imread(img_name)
    imgGray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # 灰值化
    # 二值化
    # th1 = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
    return imgGray


def contrast_image(img):
    # 对比度增强
    rows, cols = img.shape
    a = 1.4
    b = 50
    for i in range(rows):
        for j in range(cols):
            color = img[i, j] * a + b
            if color > 255:
                img[i, j] = 255
            elif color < 0:
                img[i, j] = 0
    return img


def black_image(img):
    # 黑化多余的地方
    rows, cols = img.shape
    for i in range(rows):
        for j in range(cols):
            color = img[i, j]
            if color < 200:
                img[i, j] = 0
    return img


def image_denoising(img):
    # 点降噪
    h, w = img.shape
    for y in range(1, w - 1):
        for x in range(1, h - 1):
            count = 0
            if img[x, y - 1] < 2:
                count = count + 1
            if img[x, y + 1] < 2:
                count = count + 1
            if img[x - 1, y] < 2:
                count = count + 1
            if img[x + 1, y] < 2:
                count = count + 1
            if count > 2:
                img[x, y] = 0
    return img


def image_resize(img_name, y_size=2, x_size=2):
    img = _gray_image(img_name)
    x, y = img.shape
    imgBig = cv2.resize(img, (int(y_size * y), int(x_size * x)), interpolation=cv2.INTER_CUBIC)
    return imgBig


def image_processing(img_name):
    img_big = image_resize(img_name)
    img_contrast = contrast_image(img_big)
    img_black = black_image(img_contrast)
    return img_black


def image_to_str(img):
    naked_photo = image_processing(img)
    code = pytesseract.image_to_string(naked_photo, lang="eng", config="-psm 7")
    return code


def match_image(image, templ, value):
    """在目标图片中匹配模板图片，当max_val大于0.7的时候，匹配成功"""
    info = {}

    # 匹配方式
    # methods = [cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED]
    md = cv2.TM_CCOEFF_NORMED

    th, tw = templ.shape[:2]
    result = cv2.matchTemplate(templ, image, md)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val <= value:
        return None
    if md == cv2.TM_SQDIFF_NORMED:
        tl = min_loc
    else:
        tl = max_loc
    info["result"] = (tl[0] + tw, tl[1] + th)
    return info


if __name__ == '__main__':
    # st = time.time()
    p = r'D:\2.png'
    # img = image_resize(p)
    # img = contrast_image(img)
    # img = black_image(img)
    # img = image_denoising(img)
    # img = cv2.imread(p)
    # img = image_processing(p)
    # string = pytesseract.image_to_string(img)
    # print('code:%s,type:%s' % (str_img, type(str_img)))
    # et = time.time()
    # print('total time:%s' % (et - st))
    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # print(string)
    # print(img.shape)
