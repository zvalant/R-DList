from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import os
import smtplib

import email_messages as messages

class EmailManager:
    def __init__(self):
        self.UPDATE_FILEPATH = "G:\\SW\\_Administration\\R&D Items Test\\pdfs\\EMAIL_PDFS\\R&D Sheet Update.pdf"
        self.SENDER =""
        self.SMTP_PORT = ""
        self.SMTP_SERVER = ""
        self.TITLE_UPDATE = "R&D Sheet Activity Report"
        self.SUBJECT_UPDATE = f"R&D Demand Update"
        self.msg_txt = messages.EmailMessages()
        self.msg = MIMEMultipart()
        self.msg["From"] = self.SENDER
        self.smtp_connection = smtplib.SMTP(self.SMTP_SERVER,self.SMTP_PORT)

    def send_activity_pdf(self):
        msg_txt = self.msg_txt.report
        recipients = ""
        self.msg["To"] = COMMASPACE.join(recipients)
        self.smtp_connection.starttls()
        # smtp_connection.login(sender,password)  Dont need login if its dummy email to internal network
        self.msg["Subject"] = self.SUBJECT_UPDATE
        body = f"{msg_txt}"
        self.msg.attach(MIMEText(body, "plain"))

        file_s = self.UPDATE_FILEPATH
        with open(file_s, "rb") as attachment:  # encode message
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        file_s = os.path.basename(file_s)  # removes filepath from pdf name
        part.add_header("Content-Disposition", 'attachment; filename="{}"'.format(file_s))
        self.msg.attach(part)  # attach pdf
        self.smtp_connection.sendmail(self.SENDER, recipients, self.msg.as_string())
        print(f"Message Sent for {self.SUBJECT_UPDATE}!")  # confirm email was sent
        self.smtp_connection.quit()  # log out of email
    def error_email(self,msg_txt,recipients):
        self.msg["To"] = recipients
        smtp_connection = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
        smtp_connection.starttls()
        self.msg["Subject"] = "R&D Sheet Error Found"
        body = msg_txt
        self.msg.attach(MIMEText(body,"plain"))
        self.smtp_connection.sendmail(self.SENDER,recipients,self.msg.as_string())
        self.smtp_connection.quit()








