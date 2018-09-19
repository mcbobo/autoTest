import unittest
import time
import logging
import sys
import os
from common.BSTestRunner import BSTestRunner
from common.BaseEmail import latest_report, send_mail, get_csv_data

path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)

test_dir = '../test_case'
report_dir = '../reports'

# discover = unittest.defaultTestLoader.discover(test_dir, pattern='test_login.py')

now = time.strftime('%Y-%m-%d %H_%M_%S')
report_name = report_dir + '/' + now + ' test_report.html'

with open(report_name, 'wb') as f:
    runner = BSTestRunner(stream=f, title='App Test Report', description='Android app test report')
    logging.info('start run test case...')
    # runner.run(discover)

last_report = latest_report()

user = get_csv_data(1)
send_mail(user[0], user[1], user[2], latest_report)
