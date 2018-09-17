import subprocess


def appium_start(host, port):
    bootstrap_port = str(port + 1)
    # bootstrap_port = str(port)
    cmd = 'start /b appium -a ' + host + ' -p ' + str(port) + '-bp' + str(bootstrap_port)
    print('appium service:%s' % cmd)
    # subprocess.Popen(cmd, shell=True, stdout=('../Log/' + str(port) + '.log', 'a'), stderr=subprocess.STDOUT)
    subprocess.Popen(cmd, shell=True, stdout=open('../Log/' + str(port) + '.log', 'a'), stderr=subprocess.STDOUT)
    print('appium  service at %s finished!' % port)


if __name__ == '__main__':
    host = '127.0.0.1'
    for i in range(2):
        port = 4723 + 2 * i
        appium_start(host, port)
