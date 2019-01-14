import smtplib
import email.message 
import subprocess as s
import os

def is_windows

def send_email(
    from_addr, 
    to_addr_list, 
    subject, 
    message,
    login, 
    password,
    smtpserver
):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Subject: %s\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)

    server.quit()

def notify_desktop(title, text):
    if is_windows():
        # TODO: implement desktop notifications on windows
        pass
    else:
        s.call(['notify-send',title,text])

