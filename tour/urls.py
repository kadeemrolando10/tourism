from django.conf.urls import include, url
from django.urls import path, include
from . import views

urlpatterns = [
        url(r'^$', views.index, name='base'),
        path('secretaria/', views.secretary, name='secretary'),
        path('events/', include([
                    path('', views.event_index, name='events-index'),
                    #path('new/', views.events_new, name='events-new'),
                    #path('<int:id>/edit/', views.events_edit, name='events-edit'),
                    #path('<int:id>/', views.events_show, name='events-show'),
                    #path('<int:id>/delete/', views.events_delete, name='events-delete'),
            ])),
        path('restaurants/', include([
                    path('', views.restaurant_index, name='restaurants-index'),
                    #path('new/', views.events_new, name='events-new'),
                    #path('<int:id>/edit/', views.events_edit, name='events-edit'),
                    #path('<int:id>/', views.events_show, name='events-show'),
                    #path('<int:id>/delete/', views.events_delete, name='events-delete'),
            ])),
        path('transports/', include([
                    path('', views.transport_index, name='transports-index'),
                    #path('new/', views.events_new, name='events-new'),
                    #path('<int:id>/edit/', views.events_edit, name='events-edit'),
                    #path('<int:id>/', views.events_show, name='events-show'),
                    #path('<int:id>/delete/', views.events_delete, name='events-delete'),
            ])),
        path('tourism_sites/', include([
                    path('', views.torism_site_index, name='torism_sites-index'),
                    #path('new/', views.events_new, name='events-new'),
                    #path('<int:id>/edit/', views.events_edit, name='events-edit'),
                    #path('<int:id>/', views.events_show, name='events-show'),
                    #path('<int:id>/delete/', views.events_delete, name='events-delete'),
            ])),
        path('agencys/', include([
                    path('', views.agency_index, name='agencys-index'),
                    #path('new/', views.events_new, name='events-new'),
                    #path('<int:id>/edit/', views.events_edit, name='events-edit'),
                    #path('<int:id>/', views.events_show, name='events-show'),
                    #path('<int:id>/delete/', views.events_delete, name='events-delete'),
            ])),
        path('lodgments/', include([
                    path('', views.lodgment_index, name='lodgments-index'),
                    #path('new/', views.events_new, name='events-new'),
                    #path('<int:id>/edit/', views.events_edit, name='events-edit'),
                    #path('<int:id>/', views.events_show, name='events-show'),
                    #path('<int:id>/delete/', views.events_delete, name='events-delete'),
            ])),
]
