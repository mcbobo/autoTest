import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# csv_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'account.csv')
csv_dir = '../data/mail_user.csv'


# 获取最新的报告
def latest_report():
    report_dir = os.path.join(os.path.dirname(__file__), '../Report')
    lists = os.listdir(report_dir)
    # 按时间顺序对该目录文件夹下面的文件进行排序
    lists.sort(key=lambda fn: os.path.getctime(report_dir + '\\' + fn))
    print(("new report is :" + lists[-1]))
    file = os.path.join(report_dir, lists[-1])
    return file


# 获取csv文件中指定行的数据
def get_csv_data(line, csv_file=csv_dir):
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader, 1):
            if index == line:
                return row


# 发送邮件
def send_mail(user, password, receives, text, att_path=None):
    smtpserver = 'smtp.qq.com'
    sender = user

    # 邮件内容
    subject = '自动化测试报告'
    content = '<html><p>%s</p></html>' % text
    # 构建发送与接收信息
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'html', 'utf-8'))
    msg['subject'] = subject
    msg['From'] = sender
    # msg['To'] = ','.join(receives)
    msg['To'] = receives

    # 附件内容
    if att_path:
        name = att_path
        f = open(att_path, 'rb')
        file_content = f.read()
        f.close()
        att = MIMEText(file_content, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment;filename=%s' % name.split("\\")[-1]
        msg.attach(att)

    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    smtp.helo(smtpserver)
    smtp.ehlo(smtpserver)
    smtp.login(user, password)

    print("Start send email...")
    smtp.sendmail(sender, receives, msg.as_string())
    smtp.quit()
    print("Send email end!")


if __name__ == '__main__':
    user = "3562799235@qq.com"
    pas = "gutotmnivnprcgih"
    rec = "742413096@qq.com"
    text = "测试"
    p = r"D:\1.png"
    user = get_csv_data(1)
    # att_path = latest_report()
    # send_mail(user[0], user[1], user[2], text, att_path)
