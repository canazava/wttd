from datetime import datetime
from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name = 'Bruno Canazava',
            cpf = '12345678901',
            email = 'brunocanazava@gmail.com',
            phone = '12-345678910',
        )
        self.obj.save()


    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """
        :return: Must have an auto created_at attr.
        """
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Bruno Canazava', str(self.obj))


    def test_paid_default_to_False(self):
        """
        :return: By default paid must be false
        """
        self.assertEqual(False, self.obj.paid)