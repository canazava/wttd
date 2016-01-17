from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscriptionFormClass(TestCase):
    def test_form_has_field(self):
        """
        :return: Form must have 4 fields
        """
        form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        """
        :return: DPF must only accept digits
        """
        form = self.make_validated_form(cpf='ABCD5678901')
        # self.assertFormErrorMessage(form, 'cpf', 'CPF deve conter apenas números!')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_has_11_digits(self):
        """
        :return: CPF must have 11 digits
        """
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        """
        :return: Name must be capitalized
        """
        form = self.make_validated_form(name= 'BRUNO canazava')
        self.assertEqual('Bruno Canazava', form.cleaned_data['name'])

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def make_validated_form(self, **kwargs):
        valid = dict(name='Bruno Canazava', cpf='12345678901',
                    email='brunocanazava@gmail.com', phone='12-34567-0120')
        data = dict(valid, **kwargs)

        form = SubscriptionForm(data)
        form.is_valid()
        return form