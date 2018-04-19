from django.conf.urls import include, url
from django.urls import path, include
from . import views

urlpatterns = [
        url(r'^$', views.index, name='base'),
        path('events/', include([
            path('', views.events_index, name='events-index'),
            #path('new/', views.events_new, name='events-new'),
            #path('<int:id>/edit/', views.events_edit, name='events-edit'),
            #path('<int:id>/', views.events_show, name='events-show'),
            #path('<int:id>/delete/', views.events_delete, name='events-delete'),
    ])),
]
