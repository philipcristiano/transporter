from unittest2 import TestCase
from mock import patch, Mock

from transporter.mailing_adapter import MailingAdapter
import transporter.mailing_adapter as mod



class _BaseTestMailingAdapter(TestCase):

    @patch.object(mod, 'Mailer', auto_spec=True)
    def setUp(self, mock_mailer):
        self.host = 'HOST'
        self.port = 2500
        self.mock_mailer = mock_mailer

        self.ma = MailingAdapter(self.host, self.port)

    def should_instantiate_mailer(self):
        mailer_options = {
            'manager': {
                'use': 'immediate',
            },
            'transport': {
                'use': 'smtp',
                'port': self.port,
                'host': self.host,
            }
        }
        self.mock_mailer.assert_called_once_with(mailer_options)

    def should_start_mailer(self):
        self.mock_mailer().start.assert_called_once_with()


class DescribeSendingAMailWithTheAdaptor(_BaseTestMailingAdapter):

    @patch.object(mod, 'Message', auto_spec=True)
    def setUp(self, mock_message):
        super(DescribeSendingAMailWithTheAdaptor, self).setUp()
        self.to_address = 'TO_ADDRESS'
        self.from_address = 'FROM_ADDRESS'
        self.body = 'BODY'

        self.mock_message = mock_message

        self.ma.send_mail(self.to_address, self.from_address, self.body)

    def should_instantiate_message(self):
        self.mock_message.assert_called_once_with(author=self.from_address, to=self.to_address)

    def should_attach_body_to_plain_text_of_the_message(self):
        self.assertEqual(self.mock_message().plain, self.body)

    def should_send_message_using_mailer(self):
        self.mock_mailer().send.assert_called_once_with(self.mock_message())
