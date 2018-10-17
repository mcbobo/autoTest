# coding:utf-8
import os
import socket


def check_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((host, port))
        s.shutdown(2)
    except OSError:
        print('port %s is available!' % port)
        return True
    else:
        print('port %s already be in use! ' % port)
        return False


def release_port(port):
    """释放指定的端口"""
    cmd_find = 'netstat -aon | findstr %s' % port
    result = os.popen(cmd_find).read()

    if str(port) and 'LISTENING' in result:
        """获取端口对应的pid进程"""
        i = result.index('LISTENING')
        start = i + len('LISTENING') + 7
        end = result.index('\n')
        pid = result[start:end]

        """关闭被占用端口的pid"""
        cmd_kill = 'taskkill -f -pid %s' % pid
        print(cmd_kill)
        os.popen(cmd_kill)
    else:
        print('port %s is available' % port)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 4725
    # check_port(host, port)
    # release_port(port)
    d = {'a': 1, 'b': 2}


    def f(test):
        for i in test:
            print(i)


    t = []
    t.append(d)
    print(t)
    f(t)
