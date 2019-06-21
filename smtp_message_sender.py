import smtplib


def send_mail(filepath):
    sender = 'abhangay@blusapphire.net'
    receivers = ['rpandey@blusapphire.net']

    lst = ["From: From Person <abhangay@blusapphire.net>",
           "To: To Person <rpandey@blusapphire.net>",
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
        smtpObj = smtplib.SMTP('smtp-mail.outlook.com:587')
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login("abhangay@blusapphire.net", "4bh4n94y@30-05")
        smtpObj.sendmail(sender, receivers, message)
        smtpObj.close()
        print("Successfully sent email")
    except Exception as e:
        print("Error: %s" % (e))


send_mail('Files/avransom.html')
