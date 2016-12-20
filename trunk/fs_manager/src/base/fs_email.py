# -*- coding : utf-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-08
# desc: smtp邮件发送类


import sys
import smtplib
import socket
import re    

from fs_log import *
from fs_process import *

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class Semail:
    def __init__(self,  userName = "you_name", 
                        passwd   = "you_pswd", 
                        smtpAddr = "smtp_srv_ip", 
                        smtpPort = 25,
                        fromAddr = "", 
                        toAddrs  = ""):
        self.userName = userName
        self.passwd = passwd
        self.smtpAddr = smtpAddr
        self.smtpPort = smtpPort
        self.fromAddr = fromAddr
        self.toAddrs = toAddrs
    
    def send_email_1(self, subject, text):
        
        cmd = "echo \"%s\" | mail -s \"%s\" %s" %(text, subject, self.toAddrs)
        bs_system(cmd)
    
    def send_email(self, subject, text):
        
        bRet = True
        
        text = re.sub("\n", "<br>", text)
        
        msg = MIMEMultipart()
        msg["From"] = self.fromAddr
        msg["To"]   = self.toAddrs
        msg['Subject']  = subject
        msg.attach(MIMEText(text, 'html', 'utf-8'))
        
        message = msg.as_string()
        try:
            #s = smtplib.SMTP(self.smtpAddr)
            s = smtplib.SMTP(host=self.smtpAddr, timeout= 3)
            #s.set_debuglevel(True)
            #s.connect(self.smtpAddr, self.smtpPort)
            
            s.ehlo()
            if s.has_extn('STARTTLS'):
                s.starttls()
                s.ehlo()
                
            s.login(self.userName, self.passwd)
            s.sendmail(self.fromAddr, self.toAddrs.split(","), message)
            s.quit()
        except Exception, e:
            Log.err("send email error: %s" %(str(e)))
            bRet = False
        
        return bRet
    

if __name__ == "__main__":
    try:
        email = Semail()
        email.send_email("test", "<table border=1> <tr> <td> ===test=== </td> </tr> </table>") 
    except Exception, e:
        print e
    
    
