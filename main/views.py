import datetime

from django.shortcuts import HttpResponseRedirect, reverse, render, redirect
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from main import forms, models
import logging
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

logger = logging.getLogger(__name__)


def confirm_email(request):
    if request.method =='POST':
        email_confirmation = models.EmailConfirmation.objects.get(user=request.user)
        sent_key = request.POST['email_code']
        print(sent_key, email_confirmation.sent_key)
        if sent_key == email_confirmation.sent_key:
            curr_user = request.user
            curr_user.email_confirmed = True
            curr_user.save()
            email_confirmation.status = True
            email_confirmation.confirmed_on = datetime.datetime.now()
            print(email_confirmation)
            email_confirmation.save()
            messages.info(request, 'E-mail confirmed!. Why don\'t you start with tutorials?')
            return redirect('/')
        else:
            messages.warning(request, 'Something wrong with the confirmation code?')
            return redirect('/')
    else:
        return redirect('/')


class SignUpView(FormView):
    template_name = 'sign-up.html'
    form_class = forms.UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get('next', '/')
        messages.info(self.request, 'Signed up successfully. We\'re glad to see you here!')
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get('email')
        raw_pass = form.cleaned_data.get('password1')
        logger.info('new signup for %s through SignUpView', email)
        user = authenticate(email=email, password=raw_pass)
        print(user)
        login(self.request, user)
        code = form.create_email_confirmation_code(user)
        form.send_mail(code)
        messages.info(self.request, 'Signed up successfully. We\'re glad to see you here!')
        return response



class QuestionListView(ListView):
    template_name = 'question_list.html'
    paginate_by = 4

    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None
        if tag != 'all':
            self.tag = get_object_or_404(models.Dewey, slug=tag)
        if self.tag:
            questions = models.Question.objects.filter(classification=self.tag)
        else:
            questions = models.Question.objects.all()
        return questions.order_by('created_on')


class ContactUsView(FormView):
    template_name = 'contact.html'
    form_class = forms.ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.contact_customer_service()
        return super().form_valid(form)



@login_required(login_url='/sign-in/')
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
