# coding:utf-8
import os
import csv

'''
操作文件
'''


def write_data(f, method='w+', data=""):
    if not os.path.isfile(f):
        print('文件不存在，写入数据失败')
    else:
        with open(f, method, encoding="utf-8") as fs:
            fs.write(data + "\n")


# readlines读取，返回一个可迭代的字符串列表
def read_data(f, method='r'):
    data = ''
    if not os.path.isfile(f):
        print('文件不存在，读取数据失败')
    else:
        with open(f, method) as fs:
            data = fs.readlines()
    return data


def mkdir_file(f, method='w+'):
    if not os.path.isfile(f):
        with open(f, method, encoding="utf-8") as fs:
            print("创建文件%s成功" % f)
            pass
    else:
        print("%s文件已经存在，创建失败" % f)
        pass


def remove_file(f):
    if os.path.isfile(f):
        os.remove(f)
    else:
        print("%s文件不存在，无法删除" % f)


def get_csv_data(line, csv_file='../data/mail_user.csv'):
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader, 1):
            if index == line:
                return row


if __name__ == '__main__':
    # one = get_csv_data(1)
    remove_file(r'D:/lo.txt')
