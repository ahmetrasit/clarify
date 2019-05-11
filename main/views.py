from django.shortcuts import render
from django.views.generic.edit import FormView
from main import forms

class ContactUsView(FormView):
    template_name = 'contact.html'
    form_class = forms.ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.contact_customer_service()
        return super().form_valid(form)
