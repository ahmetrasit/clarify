from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class TestPage(TestCase):
    def test_hpw(self):
        response = self.client.get(reverse('ask'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ask.html')
        self.assertContains(response, 'Clarify For Me')