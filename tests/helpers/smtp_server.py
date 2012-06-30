from multiprocessing import Process
from smtpd import SMTPServer
import asyncore


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
