import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# csv_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'account.csv')
csv_dir = '../data/mail_user.csv'


def latest_report():
    report_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
    lists = os.listdir(report_dir)
    lists.sort(key=lambda fn: os.path.getatime(report_dir + '\\' + fn))
    print("the latest report is " + lists[-1])
    file = os.path.join(report_dir, lists[-1])
    return file


def get_csv_data(line, csv_file=csv_dir):
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader, 1):
            if index == line:
                return row


def send_mail(user, password, receives, latest_report):
    f = open(latest_report, 'rb')
    mail_content = f.read()
    f.close()

    smtpserver = 'smtp.163.com'
    sender = user
    subject = 'Appium 自动化测试报告'

    msg = MIMEText(mail_content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = ','.join(receives)

    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    smtp.helo(smtpserver)
    smtp.ehlo(smtpserver)
    smtp.login(user, password)

    print("Start send email...")
    smtp.sendmail(sender, receives, msg.as_string())
    smtp.quit()
    print("Send email end!")


if __name__ == '__main__':
    csv_dir = '../data/account.csv'
    print(get_csv_data(3, csv_file=csv_dir))
