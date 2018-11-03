import smtplib
import email.message 

def sendemail(
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

def notify():
    #TODO: Implement
    print("TODO")


if __name__ == '__main__':
    sendemail(
        from_addr = 'thealexhoar@gmail.com',
        to_addr_list = ['thealexhoar@gmail.com'],
        cc_addr_list = [],
        subject = 'Test',
        message = 'Hello email world!',
        login = 'thealexhoar@gmail.com',
        password = 'kolpamgbbdwouzsh'
    )

