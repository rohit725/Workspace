#!/usr/bin/env python
import smtplib


def send_mail(filepath):
    sender = 'rpandey@blusapphire.net'
    receivers = ['rpandey516@gmail.com', 'rannarawat76448@gmail.com']

    lst = ["From: From Ranna <rpandey@blusapphire.net>",
           "To: To Rohit <rpandey516@gmail.com', 'rannarawat76448@gmail.com'>",
           "MIME-Version: 1.0",
           "Content-type: text/html",
           "Subject: SMTP HTML e-mail test",
           "",
           ""]
    with open(filepath, 'r') as f:
        html_str = f.read()

    message = "\n".join(lst)
    message += html_str

    try:
        smtpObj = smtplib.SMTP('smtp.office365.com:587')
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login("rpandey@blusapphire.net", "micr0s0ft@76448")
        smtpObj.sendmail(sender, receivers, message)
        smtpObj.close()
        print("Successfully sent email")
    except Exception as e:
        print("Error: %s" % (e))


send_mail('Files/avransom.html')
