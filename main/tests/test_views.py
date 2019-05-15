from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from django.contrib import auth
from main import forms
from main import models

# Create your tests here.
class TestPage(TestCase):
    def test_hpw(self):
        response = self.client.get(reverse('ask'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ask.html')
        self.assertContains(response, 'Clarify For Me')

    def test_signup_page_loading(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertContains(response, 's be clear.')
        self.assertIsInstance(response.context['form'], forms.UserCreationForm)

    def test_signup_submission(self):
        post_data = {'email':'deneme@deneme.com', 'password1':'abcabc12', 'password2':'abcabc12'}
        with patch.object(forms.UserCreationForm, 'send_mail') as mock_send:
            response = self.client.post(reverse('signup'), post_data)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(models.User.objects.filter(email='deneme@deneme.com').exists())
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            mock_send.assert_called_once()