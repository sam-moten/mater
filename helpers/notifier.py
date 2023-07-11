import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
smtp_server = "smtp.gmail.com" # for Gmail
port = 587  # For starttls

def send_mail(mail_context):
    
    msg = MIMEMultipart()
    msg["Subject"] = mail_context["subject"]
    msg["From"] = mail_context["sender_email"]
    msg['To'] = ", ".join(mail_context["receiver_email"])
    body_text = MIMEText(mail_context["text"], 'plain')  
    msg.attach(body_text)  # attaching the text body into msg

    context = ssl.create_default_context()
    # Try to log in to server and send email 
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # check connection
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # check connection
        server.login(mail_context["sender_email"], mail_context["password"])
        server.sendmail(mail_context["sender_email"], 
                        mail_context["receiver_email"], 
                        msg.as_string())
        # add logger...

    except Exception as e:
        print(e)
    finally:
        server.quit()