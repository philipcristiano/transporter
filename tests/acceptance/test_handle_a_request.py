from Queue import Empty
from multiprocessing import Process, Queue

from pea import *
import unittest2

from transporter.api import app
from tests.helpers.smtp_server import FakeSMTPServer


def get_mail_from_world(world):
    return world.emails.get_nowait()

@step
def I_set_the_smtp_port_to(port_number):
    world.port = port_number
    app.config['SMTP_PORT'] = port_number

@step
def I_have_a_transporter_running():
    app.config['TESTING'] = True
    world.transporter = app.test_client()

@step
def I_have_a_smtp_server_running():
    world.emails = Queue()

    world.smtp_server = FakeSMTPServer(('localhost', world.port), None)
    world.smtp_server.add_callback(world.emails.put)
    world.smtp_server_process = Process(target=world.smtp_server.asyncore_start)
    world.smtp_server_process.start()

@step
def I_send_an_http_email(to_address, from_address, body):
    data = {
        'to': to_address,
        'from': from_address,
        'text': body,
    }
    world.transporter.post('/', data=data)

@step
def I_send_an_http_email_expecting_an_error(errno):
    data = {
        'to': 'to__expecting_an_error@example.com',
        'from': 'from__expecting_an_error@example.com',
        'text': 'I was expecting a {0}'.format(errno),
    }
    resp = world.transporter.post('/', data=data)
    world.test.assertEqual(resp.status_code, errno)

@step
def I_receive_an_email_sent_to(to_address):
    email = get_mail_from_world(world)
    world.test.assertEqual(email.get('to'), to_address)

@step
def I_receive_no_emails():
    world.test.assertRaises(Empty, get_mail_from_world, world)

@step
def I_stop_the_smtp_server():
    world.smtp_server_process.terminate()


class _BaseTestCase(TestCase, unittest2.TestCase):
    def setUp(self):
        super(_BaseTestCase, self).setUp()
        world.test = self

class TestHandleASingleRequest(_BaseTestCase):
    def test_handling_a_single_request(self):
        Given.I_set_the_smtp_port_to(7999)
        And.I_have_a_transporter_running()
        And.I_have_a_smtp_server_running()
        When.I_send_an_http_email('to@example.com', 'from@example.com', 'Body')
        Then.I_receive_an_email_sent_to('to@example.com')

    def tearDown(self):
        super(TestHandleASingleRequest, self).tearDown()
        Then.I_stop_the_smtp_server()


class TestHandleASingleRequestWithNoSMTPServer(_BaseTestCase):
    def test_handling_a_single_request_with_no_SMTP_server(self):
        Given.I_set_the_smtp_port_to(7998)
        And.I_have_a_transporter_running()
        When.I_send_an_http_email_expecting_an_error(503)
        Then.I_receive_no_emails()
