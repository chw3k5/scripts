def email_caleb(subject, body_text):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    #subject   = "Test message"
    #body_text = 'body text'
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    
    body   = MIMEText(body_text)
    msg.attach(body)
    
    TO = 'chw3k5@gmail.com'
    FROM = 'thz.lab.asu@gmail.com'
    
    session = smtplib.SMTP('smtp.gmail.com', 587)
    #session = smtplib.SMTP('smtp.gmail.com', 465)
    session.ehlo()
    session.starttls()
    session.login(FROM, 'I8pi4fun')
    session.sendmail(FROM, TO, msg.as_string())
    session.quit()
    
def email_groppi(subject, body_text):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    #subject   = "Test message"
    #body_text = 'body text'
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    
    body   = MIMEText(body_text)
    msg.attach(body)
    
    TO = 'cgroppi@asu.edu'
    FROM = 'thz.lab.asu@gmail.com'
    
    session = smtplib.SMTP('smtp.gmail.com', 587)
    #session = smtplib.SMTP('smtp.gmail.com', 465)
    session.ehlo()
    session.starttls()
    session.login(FROM, 'I8pi4fun')
    session.sendmail(FROM, TO, msg.as_string())
    session.quit()
    
def text_caleb(body_text):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    #subject   = "Test message"
    #body_text = 'body text'
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = ''
    
    body   = MIMEText(body_text)
    msg.attach(body)
    
    TO = '3142838383@text.att.net'
    FROM = 'thz.lab.asu@gmail.com'
    
    session = smtplib.SMTP('smtp.gmail.com', 587)
    #session = smtplib.SMTP('smtp.gmail.com', 465)
    session.ehlo()
    session.starttls()
    session.login(FROM, 'I8pi4fun')
    session.sendmail(FROM, TO, msg.as_string())
    session.quit()