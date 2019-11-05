from flask import Flask, render_template
from flask_mail import Mail, Message
import os
app = Flask(__name__)
app.config.update(MAIL_SERVER=os.getenv('MAIL_SERVER'),
                  MAIL_PORT=os.getenv('MAIL_PORT'),
                  MAIL_USE_SSL=os.getenv('MAIL_USE_SSL'),
                  MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
                  MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
                  MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME"))
# MAIL_DEFAULT_SENDER这个配置必须跟你登录的用户名一致，所以直接设置为MAIL_USERNAME对应的值就好
mail = Mail(app)


def send_mail(subject, to, body):
    message = Message(subject, [to], body)
    mail.send(message)


def send_subscribe_mail(subject, to, **kwargs):
    message = Message(subject,
                      recipients=[to],
                      sender='Flask Weekly <%s>' % os.getenv('MAIL_USERNAME'))
    message.body = render_template('subscribe.txt', **kwargs)
    message.html = render_template('subscribe.html', **kwargs)
    mail.send(message)


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    # send_mail('Subscribe success', 'oz_myx@126.com',
    #           'Hello,thank you to subscribe my chanel')
    send_subscribe_mail('Subscribe Success', 'oz_myx@126.com')
    return 'GOGOGO'
