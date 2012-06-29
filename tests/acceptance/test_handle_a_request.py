from multiprocessing import Process, Queue
from smtpd import SMTPServer
import asyncore

from pea import *

from transporter.api import app



class FakeSMTPServer(SMTPServer):
    def __init__(self, emails, *args, **kwargs):
        self.emails = emails
        SMTPServer.__init__(self, *args, **kwargs)

    def process_message(self, peer, mailfrom, rcpttos, data):
        self.emails.put((mailfrom, rcpttos, data))

    def asyncore_start(self):
        try:
            asyncore.loop()
        finally:
            print 'Stopping asyncore'


def get_mail_from_world(world):
    return world.emails.get_nowait()

@step
def I_have_a_transporter_running():
    app.config['TESTING'] = True
    world.transporter = app.test_client()

@step
def I_have_a_smtp_server_running():
    world.emails = Queue()

    world.smtp_server = FakeSMTPServer(world.emails, ('localhost', 7999), None)
    world.smtp_server_process = Process(target=world.smtp_server.asyncore_start)
    world.smtp_server_process.start()

@step
def I_send_an_http_email(to_address, from_address, body):
    data = {
        'to_address': to_address,
        'from_address': from_address,
        'body': body,
    }
    world.transporter.post('/', data=data)

@step
def I_receive_an_email_sent_to(to_address):
    email = get_mail_from_world(world)
    assert email[1][0] == to_address

@step
def I_stop_the_smtp_server():
    world.smtp_server_process.terminate()


class TestHandleASingleRequest(TestCase):
    def test_running_a_single_process(self):
        Given.I_have_a_transporter_running()
        And.I_have_a_smtp_server_running()
        When.I_send_an_http_email('to@example.com', 'from@example.com', 'Body')
        Then.I_receive_an_email_sent_to('to@example.com')

    def tearDown(self):
        Then.I_stop_the_smtp_server()
