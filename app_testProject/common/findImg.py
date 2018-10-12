import cv2
import numpy as np


def match_image(image, templ, value):
    """在目标图片中匹配模板图片，当max_val大于0.7的时候，匹配成功"""
    info = {}
    tpl = cv2.imread(templ)
    target = cv2.imread(image)
    target = cv2.resize(target, (500, 900))

    # 匹配方式
    # methods = [cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED]
    md = cv2.TM_CCOEFF_NORMED

    # 获得模板的高宽
    th, tw = tpl.shape[:2]
    result = cv2.matchTemplate(target, tpl, md)
    # 寻找矩阵(一维数组当作向量,用Mat定义) 中最小值和最大值的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val <= value:
        return None

    if md == cv2.TM_SQDIFF_NORMED:
        tl = min_loc
    else:
        tl = max_loc
    info['result'] = (tl[0] + tw, tl[1] + th)
    return info
    # cv2.rectangle(target, tl, br, (0, 0, 255), 2)
    # cv2.imshow('match-' + np.str(md), target)


imobj = r'D:\soft\pyc\auto_appium\app_testProject\data\element\search.png'
imsrc = r"D:\Hlddz\t1.png"
# print(match_image(imsrc, imobj, 0.7).get("result"))

from common.BaseImage import match_image

tem = cv2.imread(imobj)
tar = cv2.imread(imsrc)
tar = cv2.resize(tar, (500, 900))
print(match_image(tar, tem, 0.7))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
