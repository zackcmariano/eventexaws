from django.core import mail
from django.test import TestCase
from subscriptions.forms import SubscriptionForm
from subscriptions.models import Subscription

class SubscribeGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """Get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)
    
    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Zack Mariano', cpf='12345678901', email='zack.cmariano@gmail.com', phone='16-99218-9218')
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/1/"""
        self.assertRedirects(self.response, '/inscricao/1/')

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)
    
    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())

