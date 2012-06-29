from flask import Flask, request
app = Flask(__name__)
from marrow.mailer import Mailer, Message

def send_mail(to_address, from_address, body):
    mailer = Mailer(dict(
            manager = 'immediate',
            transport = dict(
                    use = 'smtp',
                    port = 7999,
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
    send_mail(f['to_address'], f['from_address'], f['body'])

    return 'Yay!'


if __name__ == "__main__":
    app.run()
