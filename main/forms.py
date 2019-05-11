from django import forms
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)
class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=128)
    message = forms.CharField(label='About', max_length=512, widget=forms.Textarea)

    def contact_customer_service(self):
        logger.info('contacting customer service')
        message = '{}\n{}'.format(self.cleaned_data['name'], self.cleaned_data['message'])
        send_mail('Customer service', message, 'site_contact@clarify4me.com', ['customer_service@clarify4me.com', 'ahmetrasit'], fail_silently=False)

