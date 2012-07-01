"The object that sends mail"
from marrow.mailer import Mailer, Message


class MailingAdapter(object):

    def __init__(self, host, port):

        self.mailer = Mailer(dict(
                manager = 'immediate',
                transport = dict(
                        use = 'smtp',
                        port = port,
                        host = 'localhost')))
        self.mailer.start()

    def send_mail(self, to_address, from_address, body):

        message = Message(author=from_address, to=to_address)
        message.subject = "Testing Marrow Mailer"
        message.plain = body
        self.mailer.send(message)
