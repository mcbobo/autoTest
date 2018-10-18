import pickle
import os


def file_status(fun):
    def wrapper(path):
        if not os.path.isfile(path):
            with open(path, 'w+', encoding="utf-8") as fs:
                print("创建%s文件成功" % path)
                pass
        return fun(path)

    return wrapper


def write(data, path="data.pickle"):
    with open(path, 'wb') as f:
        pickle.dump(data, f, 0)


def read(path):
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
        except EOFError:
            data = {}
    return data


@file_status
def readInfo(path):
    # data = []
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
            print(data)
        except EOFError:
            data = []
    return data


def writeInfo(data="", path="data.pickle"):
    """

    :type data: dict
    """
    _read = readInfo(path)
    result = []
    if _read:
        _read.append(data)
        result = _read
    else:
        result.append(data)
    with open(path, 'wb') as f:
        pickle.dump(result, f)


if __name__ == "__main__":
    # write("用例失败重连过一次，失败原因：", "../Log/connect64dd15b8-ca91-11e7-87ae-38c98647adce.pickle")
    # a = readInfo(r'D:\Appium\AutoTest\auto_appium\app_testProject\Log\devices.pickle')
    # b = readInfo(r'D:\Appium\AutoTest\auto_appium\app_testProject\Log\info.pickle')
    b = readInfo(r'D:\Appium\AutoTest\auto_appium\app_testProject\Log\sum.pickle')
    pass
