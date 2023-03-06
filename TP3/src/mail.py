import os
import smtplib, ssl
from email.message import EmailMessage
import configparser

def send(to,code):
    config = configparser.ConfigParser()
    config.read(os.path.abspath('../config.ini'))
    sender_email = config['Mail']['user']
    password = config['Mail']['password']
    
    msg = EmailMessage()
    msg.set_content(code)
    msg['Subject'] = 'Código de acesso'
    msg['From'] = sender_email
    msg['To'] = to

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls(context=context) # Secure the connection
        server.login(sender_email, password)
        server.send_message(msg)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()
