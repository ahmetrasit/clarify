from django.test import TestCase
from django.core import mail
from main import forms

class TestForm(TestCase):
    def test_valid_contact_customer_service(self):
        form = forms.ContactForm({'name':'Me Myself', 'message':'how a ya'})
        self.assertTrue(form.is_valid())

        with self.assertLogs('main.forms', level='INFO') as sm:
            form.contact_customer_service()
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].subject, 'Customer service')
            self.assertGreaterEqual(len(sm.output), 1)

    def test_invalid_contact_customer_service(self):
        form = forms.ContactForm({'name':'Me Myself and Irene'})
        self.assertFalse(form.is_valid())

    def test_valid_signup_form_sends_email(self):
        form = forms.UserCreationForm(  {'email':'deneme@deneme.com',
                                        'password1':'abcabc12',
                                        'password2':'abcabc12'})
        self.assertTrue(form.is_valid())
        with self.assertLogs('main.forms', level='INFO') as sm:
            form.send_mail()
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].subject, 'Welcome to clarification!')
            self.assertGreaterEqual(len(sm.output), 1)
