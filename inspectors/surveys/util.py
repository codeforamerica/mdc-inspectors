from flask_mail import Message
from inspectors.extensions import mail


def send_email(subject, recipients, text_body, html_body=None):
    ''' E-mail utility function.
    '''
    msg = Message(
        subject,
        recipients=recipients)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    mail.send(msg)
