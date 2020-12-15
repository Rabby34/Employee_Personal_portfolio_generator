import pro_pic_adder
import text_on_final_picture_output

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import set_name as mail_info
To_mail=mail_info.to_mail()
Cc_mail=mail_info.cc_mail()

# -------------------------- Group email ----------------------------
msgRoot = MIMEMultipart('related')
me = ''        # provide from email
to = To_mail
cc = Cc_mail
bcc = ['md.fazle.rabby34@gmail.com', '']

recipient = to + cc + bcc

subject = "Your Month Infographical Work Status Report Till Now"

email_server_host = ''        #provide mail server
port = 25

msgRoot['From'] = me

msgRoot['To'] = ', '.join(to)
msgRoot['Cc'] = ', '.join(cc)
msgRoot['Bcc'] = ', '.join(bcc)
msgRoot['Subject'] = subject

msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

msgText = MIMEText("""
                       <img src="cid:full_report" height='1935', width='1270'><br>

                       """, 'html')

msgAlternative.attach(msgText)

# --------- Set Credit image in mail   -----------------------
fp = open('./images/send_this_photo.png', 'rb')
img1_2 = MIMEImage(fp.read())
fp.close()

img1_2.add_header('Content-ID', '<full_report>')
msgRoot.attach(img1_2)

# # ----------- Finally send mail and close server connection ---
print('-----------------------------------------------')
print('sending mail')
server = smtplib.SMTP(email_server_host, port)
server.ehlo()
server.sendmail(me, recipient, msgRoot.as_string())
server.close()
print('mail sent')
print('-----------------------------------------------')
