'''
Created on Feb 14, 2019

@author: LONGBRIDGE
'''
from email.mime.text import MIMEText
import smtplib

def send_email(email,height,average_height,count):
    from_email = "adeniranjohn93@gmail.com"
    from_password="kayode89"
    to_email = email
    
    subject = "height data"
    mess = "Hey There,your height is <strong> %s</strong>,Average height of all is <strong>%s</strong> and calculated after a total count of<strong> %s</strong> " % (height,average_height,count)
    msg = MIMEText(mess, 'html')
    msg['subject']= subject
    msg['To']= to_email
    msg['From']= from_email
    
    
    gmail = smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_password)
    gmail.send_message(msg)
    
    