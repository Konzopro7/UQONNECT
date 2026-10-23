from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [path('admin/', admin.site.urls), path('', views.home, name='home'), path('a-propos/', views.about, name='about'), path('evenements/', views.events, name='events'), path('evenements/<slug:slug>/', views.event_detail, name='event_detail'), path('evenements/<slug:slug>/calendrier.ics', views.event_ics, name='event_ics'), path('projets/', views.projects, name='projects'), path('actualites/', views.articles, name='articles'), path('actualites/<slug:slug>/', views.article_detail, name='article_detail'), path('contact/', views.contact, name='contact'), path('sitemap.xml', views.sitemap, name='sitemap'), path('robots.txt', views.robots, name='robots')]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
