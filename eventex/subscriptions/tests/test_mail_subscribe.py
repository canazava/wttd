from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribeValid(TestCase):
    def setUp(self):
        data = dict(name='Bruno Canazava', cpf='12345678901',
                    email='brunocanazava@gmail.com', phone='12-34567-0120')
        self.client.post(r('subscriptions:new'), data)
        self.mail = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.mail.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.mail.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'brunocanazava@gmail.com']

        self.assertEqual(expect, self.mail.to)

    def test_subscription_email_body(self):

        contents = ['Bruno Canazava',
                    '12345678901',
                    'brunocanazava@gmail.com',
                    '12-34567-0120',
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.mail.body)