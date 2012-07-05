"""Test against a real SMTP server as Marrow.Mailer is an external library.

"""

from unittest2 import TestCase
from multiprocessing import Process, Queue

from transporter.mailing_adapter import MailingAdapter
from tests.helpers.smtp_server import FakeSMTPServer


class TestMailingAdapter(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.queue = Queue()
        port = 7000
        cls.mailing_adapter = MailingAdapter('localhost', port)
        cls._start_smtp_server_in_a_new_process(port, cls.queue.put)

        cls.mailing_adapter.send_mail(
            'to@example.com',
            'from@example.com',
            'Plain text body'
        )
        cls.emails = []
        while not cls.queue.empty():
            cls.emails.append(cls.queue.get())

    @classmethod
    def _start_smtp_server_in_a_new_process(cls, port, callback):
        cls.server = FakeSMTPServer

        cls.smtp_server = FakeSMTPServer(('localhost', port), None)
        cls.smtp_server.add_callback(callback)
        cls.smtp_server_process = Process(target=cls.smtp_server.asyncore_start)
        cls.smtp_server_process.start()

    @classmethod
    def tearDownClass(cls):
        cls._stop_smtp_server_process()

    @classmethod
    def _stop_smtp_server_process(cls):
        cls.smtp_server_process.terminate()

    def test_a_mail_was_received(self):
        self.assertEquals(len(self.emails), 1)
