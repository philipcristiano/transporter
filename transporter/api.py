import errno
import socket

from flask import abort, Flask, request
from marrow.mailer import Mailer, Message


app = Flask(__name__)

def send_mail(to_address, from_address, body):
    mailer = Mailer(dict(
            manager = 'immediate',
            transport = dict(
                    use = 'smtp',
                    port = app.config['SMTP_PORT'],
                    host = 'localhost')))
    mailer.start()

    message = Message(author=from_address, to=to_address)
    message.subject = "Testing Marrow Mailer"
    message.plain = body
    mailer.send(message)

    mailer.stop()

@app.route('/', methods=['POST'])
def handle_mail():
    f = request.form

    try:
        send_mail(f['to_address'], f['from_address'], f['body'])
    except socket.error, v:
        errorcode=v[0]
        if errorcode==errno.ECONNREFUSED:
            abort(503)
    return 'Yay!'


if __name__ == "__main__":
    app.run()
