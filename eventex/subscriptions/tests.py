from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):

    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """
        :return: Get /inscricao/ must return status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        :return: Must use subscriptions/subscription_form.html
        """
        self.assertTemplateUsed((self.resp, 'subscriptions/subscription_form.html'))

    def test_html(self):
        """
        :return: HTML must contain input tags
        """
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """
        :return: HTML must contains csrf
        """
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """
        :return:Context must have subscription form
        """
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_field(self):
        """
        :return: Form must have 4 fields
        """
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))



class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Bruno Canazava', cpf='12345678901',
                    email='brunocanazava@gmail.com', phone='12-34567-0120')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """
        :return: Valid POST should redirect to /inscricao/
        """
        self.assertEqual(302, self.resp.status_code)


    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'brunocanazava@gmail.com']

        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Bruno Canazava', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('brunocanazava@gmail.com', email.body)
        self.assertIn('12-34567-0120', email.body)


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """
        :return: Invalid POST should not redirect
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp,
                                'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Bruno Canazava', cpf='12345678901',
                    email='brunocanazava@gmail.com', phone='12-34567-0120')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição Reliazada com sucesso!')





























