from multiprocessing import Process
from smtpd import SMTPServer
from email.parser import FeedParser
import asyncore


class FakeSMTPServer(SMTPServer):
    "SMTP server that will take a message and call listeners"
    def __init__(self, *args, **kwargs):
        SMTPServer.__init__(self, *args, **kwargs)
        self.callbacks = []

    def process_message(self, peer, mailfrom, rcpttos, data):
        message = self._parse_message(data)
        for callback in self.callbacks:
            callback(message)

    def _parse_message(self, message):
        parser = FeedParser()
        parser.feed(message)
        return parser.close()

    def asyncore_start(self):
        try:
            asyncore.loop()
        finally:
            print 'Stopping asyncore'

    def add_callback(self, callback):
        "Callback that will receive the email tuple"
        self.callbacks.append(callback)
