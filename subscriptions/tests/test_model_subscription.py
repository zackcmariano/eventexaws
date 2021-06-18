from datetime import datetime
from django.test import TestCase
from subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Zack Mariano',
            cpf='12345678901',
            email='zack.cmariano@gmail.com',
            phone='16-99218-9218'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attr."""
        self.assertIsInstance(self.obj.created_at, datetime)