from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('projects/', views.projects_page, name='projects'),
    path('skills/', views.skills_page, name='skills'),
    path('services/', views.services_page, name='services'),
    path('contact/', views.contact_page, name='contact'),
    path('about/', views.about_page, name='about'),
    path('send-quote-email/', views.send_quote_email, name='send_quote_email'),
]
