import random
import string

def get_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def get_random_hero():
    img = random.randint(1,10)
    return 'h' + str(img) + '.jpg'

def get_random_profile_pic():
    img = random.randint(1,8)
    return '/images/p' + str(img) + '.jpg'

def send_subscriber_mail(c_email):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        mail_content = '''Thank you for selecting us. You will get notificatoin from this email .,make sure to check spam folder if not.'''

        #The mail addresses and password
        sender_address = 'info.devblogs@gmail.com' ## change this 
        sender_pass = os.environ.get("G_PASS") ## change this 
        receiver_address = c_email

        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'successfully subscribed for dev-blogs'   #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
      