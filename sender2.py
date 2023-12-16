from email.message import EmailMessage
import ssl
import smtplib
from datetime import datetime
import random
#sender Credentials
email_sender = "binanceworkspace0@gmail.com"
email_password = "npny fonr kcvv wujd"

def send(Name, Email):
    
    email_receiver_name = Name
    email_receiver = Email

    email_subject = "Account Created Successfully !"

    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    random_number = random.randrange(10**7, 10**8)

    email_body = f"""
    Dear {email_receiver_name},

    We are pleased to inform you that your account has been successfully created!

    Acount Details:
    - Name : {Name}
    - Email - {Email}
    - Date & Time: {current_date_time}

    Thank you for choosing us! We look forward to serving you. Your Temporary id is ( {random_number} ).

    Best regards,
    Vision Optical
    visionoptical.shop

    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = email_subject
    em.set_content(email_body)

    #set the context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    print("Email sent successfully!")