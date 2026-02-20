from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),          # Home page
    path('projects/', views.projects_page, name='projects'),  # Projects page
    path('skills/', views.skills_page, name='skills'),        # Skills page
    path('services/', views.services_page, name='services'),  # Services page
    path('contact/', views.contact_page, name='contact'),     # Contact page
    path('about/', views.about_page, name='about'),           # About page
      path('send-quote-email/', views.send_quote_email, name='send_quote_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
