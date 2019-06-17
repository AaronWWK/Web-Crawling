
# SMTP是发送邮件的协议，Python内置对SMTP的支持，可以发送纯文本邮件、HTML邮件以及带附件的邮件。
# Python对SMTP支持有smtplib和email两个模块，email负责构造邮件，smtplib负责发送邮件。


def send_email(mes):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    # 第三方 SMTP 服务
    mail_host="smtp.163.com"  #设置服务器
    # mail_host="localhost"
      #设置服务器
    mail_user="sywanwei1103@163.com"    #用户名
    mail_pass="sy6980310"   #口令


    sender = 'sywanwei1103@163.com'
    receivers = ['453130895@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(mes,'plain', 'utf-8')
    message['From'] = '<sywanwei1103@163.com>' #Header("菜鸟教程", 'utf-8')
    message['To'] =  '453130895@qq.com' # Header("测试", 'utf-8')

    subject = 'Do you want to go out tonight?'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 1025)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print( "邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")
send_email('What about at bods 7 pm')


import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host="smtp.163.com"  #设置服务器
# mail_host="localhost"
  #设置服务器
mail_user="sywanwei1103@163.com"    #用户名
mail_pass="sy6980310"   #口令


sender = 'sywanwei1103@163.com'
receivers = ['453130895@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
mes='this is an inviation'
message = MIMEText(mes,'plain', 'utf-8')
message['From'] = '<sywanwei1103@163.com>' #Header("菜鸟教程", 'utf-8')
message['To'] =  '453130895@qq.com' # Header("测试", 'utf-8')
message['Cc'] = '<sywanwei1103@163.com>'

subject = 'Do you want to go out tonight?'
message['Subject'] = Header(subject, 'utf-8')

smtpObj = smtplib.SMTP()
smtpObj.UseDefaultCredentials = True
smtpObj.EnableSsl = True
smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
smtpObj.login(mail_user,mail_pass)
smtpObj.sendmail(sender, receivers, message.as_string())
