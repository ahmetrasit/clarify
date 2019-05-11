
from django.urls import path
from django.views.generic import TemplateView
from main import views

urlpatterns = [
    path('about-us/', TemplateView.as_view(template_name='about_us.html'), name='about_us'),
    path('', TemplateView.as_view(template_name='ask.html'), name='home'),
    path('ask/', TemplateView.as_view(template_name='ask.html'), name='ask'),
    path('contact/', views.ContactUsView.as_view(), name='contact')

]