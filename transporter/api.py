import errno
import socket

from flask import abort, Flask, request

from transporter.mailing_adapter import MailingAdapter

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_mail():
    f = request.form
    mailing_adapter = MailingAdapter('localhost', app.config['SMTP_PORT'])

    try:
        mailing_adapter.send_mail(f['to'], f['from'], f['text'])
    except socket.error, v:
        errorcode=v[0]
        if errorcode==errno.ECONNREFUSED:
            abort(503)
    return 'Yay!'


if __name__ == "__main__":
    app.run()
