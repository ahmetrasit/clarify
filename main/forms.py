from django import forms
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import authenticate
from . import models
import logging
from random import randint

logger = logging.getLogger(__name__)


class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(strip=False, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email is not None and password:
            self.user = authenticate(self.request, email=email, password=password)
            if self.user is None:
                raise forms.ValidationError('Invalid e-mail or password.')
            logger.info(f'{self.user} is logged in')
        return self.cleaned_data

    def get_user(self):
        return self.user





class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=128)
    message = forms.CharField(label='About', max_length=512, widget=forms.Textarea)

    def contact_customer_service(self):
        logger.info('contacting customer service')
        message = '{}\n{}'.format(self.cleaned_data['name'], self.cleaned_data['message'])
        send_mail('Customer service', message, 'site_contact@clarify4me.com', ['customer_service@clarify4me.com', 'ahmetrasit'], fail_silently=False)


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = models.User
        fields = ('email',)
        field_classes = {'email':UsernameField}

    def create_email_confirmation_code(self, user):
        random_code = randint(111111, 999999)
        confirmation = models.EmailConfirmation(user=user, sent_key=random_code)
        confirmation.save()
        return random_code

    def send_mail(self, code):
        logger.info('sending sign-up email for %s', self.cleaned_data['email'])

        message = 'Welcome {}! Please enter the following code to confirm your e-mail address: {} '.format(self.cleaned_data['email'], code)
        send_mail('Welcome to clarification!', message, 'welcome@clarify4me.com',
                  [self.cleaned_data['email']], fail_silently=True)