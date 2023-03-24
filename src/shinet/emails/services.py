"""

"""
from django.core.mail import send_mail

send_mail(
    'Subject here',
    'Here is the message.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)

# import smtplib
# from email.message import EmailMessage
# from config import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT
#
#
# def send_mail(message, mail_to):
#     server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
#     server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
#     email = EmailMessage()
#     email['From'] = EMAIL_HOST_USER
#     email['To'] = mail_to
#     email['Subject'] = "Подтверждение регистрации в Bookbot21"
#     email.set_content(message)
#     server.send_message(email)
#


