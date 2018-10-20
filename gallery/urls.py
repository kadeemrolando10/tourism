from django.conf.urls import include, url
from django.contrib.auth import logout
from django.urls import path, include
from tour_site import settings
from . import views

urlpatterns = [
    path('gallery/', views.index, name='gallery')
    ]