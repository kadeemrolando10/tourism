from django.conf.urls import include, url
from django.contrib.auth import logout
from django.urls import path, include
from tour_site import settings
from . import views

urlpatterns = [
    url(r'^$', views.index, name='base'),
    path('index_admin/', views.index_admin, name='index_admin'),
    path('notifications/', views.notification, name='notifications'),
    path('<int:id>/change', views.change_main, name='change-id-main'),
    path('<int:id>/change-site', views.change_main_tourism_site, name='change_main_tourism_site'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    path('users/', include([
        path('', views.user_index, name='user-index'),
        path('new/', views.user_new, name='user-new'),
        path('<int:id>/', views.user_show, name='user-show'),
        path('<int:id>/edit/', views.user_edit, name='user-edit'),
        path('<int:id>/delete/', views.user_delete, name='user-delete'),
    ])),
    path('configurations/', include([
        path('', views.configuration_index, name='configurations-index'),
        path('objectives/', include([
            path('new/', views.objective_new, name='objectives-new'),
            path('<int:id>/edit/', views.objective_edit, name='objectives-edit'),
            path('<int:id>/delete/', views.objective_delete, name='objectives-delete'),
        ])),
        path('secretary/', include([
            path('new/', views.secretary_new, name='secretaries-new'),
            path('<int:id>/edit/', views.secretary_edit, name='secretaries-edit'),
            path('<int:id>/delete/', views.secretary_delete, name='secretaries-delete'),
        ])),
        path('functions/', include([
            path('new/', views.function_new, name='functions-new'),
            path('<int:id>/edit/', views.function_edit, name='functions-edit'),
            path('<int:id>/delete/', views.function_delete, name='functions-delete'),
            path('<int:id>/active/', views.function_active_admin, name='functions-active-admin'),
            path('<int:id>/inactive/', views.function_inactive_admin, name='functions-inactive-admin'),
        ])),
        path('laws/', include([
            path('new/', views.law_new, name='laws-new'),
            path('<int:id>/edit/', views.law_edit, name='laws-edit'),
            path('<int:id>/delete/', views.law_delete, name='laws-delete'),
            path('<int:id>/active/', views.law_active_admin, name='laws-active-admin'),
            path('<int:id>/inactive/', views.law_inactive_admin, name='laws-inactive-admin'),
        ])),
        path('socials/', include([
            path('new/', views.social_new, name='socials-new'),
            path('<int:id>/edit/', views.social_edit, name='socials-edit'),
            path('<int:id>/delete/', views.social_delete, name='socials-delete'),
        ])),
    ])),
    path('secretary/', views.secretary, name='secretary'),

    path('assignments/', include([
        path('', views.assignments_index, name='assignments-index'),
        path('sites/', include([
            path('new/', views.assignment_site_new, name='assignment_sites-new'),
            path('<int:id>/edit/', views.assignment_site_edit, name='assignment_sites-edit'),
            path('<int:id>/delete/', views.assignment_site_delete, name='assignment_sites-delete'),
        ])),
        path('transports/', include([
            path('new/', views.assignment_transport_new, name='assignment_transports-new'),
            path('<int:id>/edit/', views.assignment_transport_edit, name='assignment_transports-edit'),
            path('<int:id>/delete/', views.assignment_transport_delete, name='assignment_transports-delete'),
        ])),
        path('agencies/', include([
            path('new/', views.assignment_agency_new, name='assignment_agencies-new'),
            path('<int:id>/edit/', views.assignment_agency_edit, name='assignment_agencies-edit'),
            path('<int:id>/delete/', views.assignment_agency_delete, name='assignment_agencies-delete'),
        ])),
        path('restaurants/', include([
            path('new/', views.assignment_restaurant_new, name='assignment_restaurants-new'),
            path('<int:id>/edit/', views.assignment_restaurant_edit, name='assignment_restaurants-edit'),
            path('<int:id>/delete/', views.assignment_restaurant_delete, name='assignment_restaurants-delete'),
        ])),
        path('lodgings/', include([
            path('new/', views.assignment_lodging_new, name='assignment_lodgings-new'),
            path('<int:id>/edit/', views.assignment_lodging_edit, name='assignment_lodgings-edit'),
            path('<int:id>/delete/', views.assignment_lodging_delete, name='assignment_lodgings-delete'),

        ])),
    ])),

    path('location/', include([
        path('', views.location_index_admin, name='location-index-admin'),
        path('<int:id>/', views.location_show_admin, name='location-show-admin'),
        path('new/', views.location_new_admin, name='location-new-admin'),
        path('<int:id>/edit/', views.location_edit_admin, name='location-edit-admin'),
        path('<int:id>/delete/', views.location_delete_admin, name='location-delete-admin'),
    ])),

    path('agencies/', include([
        path('', views.agency_index, name='agencies-index'),
        path('<int:id>/', views.agency_show, name='agencies-show'),
        path('agencies-admin/', include([
            path('', views.agency_index_admin, name='agencies-index-admin'),
            path('<int:id>/', views.agency_show_admin, name='agencies-show-admin'),
            path('new/', views.agency_new_admin, name='agencies-new-admin'),
            path('<int:id>/edit/', views.agency_edit_admin, name='agencies-edit-admin'),
            path('<int:id>/delete/', views.agency_delete_admin, name='agencies-delete-admin'),
            path('<int:id>/active/', views.agency_active_admin, name='agencies-active-admin'),
            path('<int:id>/inactive/', views.agency_inactive_admin, name='agencies-inactive-admin'),

            path('service-admin/', include([
                path('', views.agency_service_index_admin, name='agencies-services-index-admin'),
                path('<int:id>/', views.agency_service_show_admin, name='agencies-services-show-admin'),
                path('new/', views.agency_service_new_admin, name='agencies-services-new-admin'),
                path('<int:id>/edit/', views.agency_service_edit_admin, name='agencies-services-edit-admin'),
                path('<int:id>/delete/', views.agency_service_delete_admin, name='agencies-services-delete-admin'),
            ])),
            path('schedule-admin/', include([
                path('', views.agency_schedule_index_admin, name='agencies-schedules-index-admin'),
                path('<int:id>/', views.agency_schedule_show_admin, name='agencies-schedules-show-admin'),
                path('new/', views.agency_schedule_new_admin, name='agencies-schedules-new-admin'),
                path('<int:id>/edit/', views.agency_schedule_edit_admin, name='agencies-schedules-edit-admin'),
                path('<int:id>/delete/', views.agency_schedule_delete_admin, name='agencies-schedules-delete-admin'),
            ])),
        ])),
    ])),

    path('events/', include([
        path('', views.event_index, name='events-index'),
        path('events-admin/', include([
            path('', views.event_index_admin, name='events-index-admin'),
            path('<int:id>/', views.event_show_admin, name='events-show-admin'),
            path('new/', views.event_new_admin, name='events-new-admin'),
            path('<int:id>/edit/', views.event_edit_admin, name='events-edit-admin'),
            path('<int:id>/delete/', views.event_delete_admin, name='events-delete-admin'),
            path('<int:id>/active/', views.event_active_admin, name='events-active-admin'),
            path('<int:id>/inactive/', views.event_inactive_admin, name='events-inactive-admin'),
        ])),
    ])),

    path('restaurants/', include([
        path('', views.restaurant_index, name='restaurants-index'),
        path('<int:id>/', views.restaurant_show, name='restaurants-show'),

        path('restaurants-admin/', include([
            path('', views.restaurant_index_admin, name='restaurants-index-admin'),
            path('<int:id>/', views.restaurant_show_admin, name='restaurants-show-admin'),
            path('new/', views.restaurant_new_admin, name='restaurants-new-admin'),
            path('<int:id>/edit/', views.restaurant_edit_admin, name='restaurants-edit-admin'),
            path('<int:id>/delete/', views.restaurant_delete_admin, name='restaurants-delete-admin'),
            path('<int:id>/active/', views.restaurant_active_admin, name='restaurants-active-admin'),
            path('<int:id>/inactive/', views.restaurant_inactive_admin, name='restaurants-inactive-admin'),

            path('service-admin/', include([
                path('', views.restaurant_service_index_admin, name='restaurants-services-index-admin'),
                path('<int:id>/', views.restaurant_service_show_admin, name='restaurants-services-show-admin'),
                path('new/', views.restaurant_service_new_admin, name='restaurants-services-new-admin'),
                path('<int:id>/edit/', views.restaurant_service_edit_admin, name='restaurants-services-edit-admin'),
                path('<int:id>/delete/', views.restaurant_service_delete_admin,
                     name='restaurants-services-delete-admin'),
            ])),
            path('menu-admin/', include([
                path('', views.restaurant_menu_index_admin, name='restaurants-menus-index-admin'),
                path('<int:id>/', views.restaurant_menu_show_admin, name='restaurants-menus-show-admin'),
                path('new/', views.restaurant_menu_new_admin, name='restaurants-menus-new-admin'),
                path('<int:id>/edit/', views.restaurant_menu_edit_admin, name='restaurants-menus-edit-admin'),
                path('<int:id>/delete/', views.restaurant_menu_delete_admin, name='restaurants-menus-delete-admin'),
            ])),
            path('schedule-admin/', include([
                path('', views.restaurant_schedule_index_admin, name='restaurants-schedules-index-admin'),
                path('<int:id>/', views.restaurant_schedule_show_admin, name='restaurants-schedules-show-admin'),
                path('new/', views.restaurant_schedule_new_admin, name='restaurants-schedules-new-admin'),
                path('<int:id>/edit/', views.restaurant_schedule_edit_admin, name='restaurants-schedules-edit-admin'),
                path('<int:id>/delete/', views.restaurant_schedule_delete_admin,
                     name='restaurants-schedules-delete-admin'),
            ])),
        ])),
    ])),

    path('transports/', include([
        path('', views.transport_index, name='transports-index'),
        path('<int:id>/', views.transport_show, name='transports-show'),
        path('transports-admin/', include([
            path('', views.transport_index_admin, name='transports-index-admin'),
            path('<int:id>/', views.transport_show_admin, name='transports-show-admin'),
            path('new/', views.transport_new_admin, name='transports-new-admin'),
            path('<int:id>/edit/', views.transport_edit_admin, name='transports-edit-admin'),
            path('<int:id>/delete/', views.transport_delete_admin, name='transports-delete-admin'),
            path('<int:id>/active/', views.transport_active_admin, name='transports-active-admin'),
            path('<int:id>/inactive/', views.transport_inactive_admin, name='transports-inactive-admin'),

            path('destination-admin/', include([
                path('', views.transport_destination_index_admin, name='transports-destination-index-admin'),
                path('<int:id>/', views.transport_destination_show_admin, name='transports-destination-show-admin'),
                path('new/', views.transport_destination_new_admin, name='transports-destination-new-admin'),
                path('<int:id>/edit/', views.transport_destination_edit_admin,
                     name='transports-destination-edit-admin'),
                path('<int:id>/delete/', views.transport_destination_delete_admin,
                     name='transports-destination-delete-admin'),
            ])),
            path('service-admin/', include([
                path('', views.transport_service_index_admin, name='transports-services-index-admin'),
                path('<int:id>/', views.transport_service_show_admin, name='transports-services-show-admin'),
                path('new/', views.transport_service_new_admin, name='transports-services-new-admin'),
                path('<int:id>/edit/', views.transport_service_edit_admin, name='transports-services-edit-admin'),
                path('<int:id>/delete/', views.transport_service_delete_admin, name='transports-services-delete-admin'),
            ])),
            path('type-service-admin/', include([
                path('', views.transport_type_service_index_admin, name='transports-type-services-index-admin'),
                path('<int:id>/', views.transport_type_service_show_admin, name='transports-type-services-show-admin'),
                path('new/', views.transport_type_service_new_admin, name='transports-type-services-new-admin'),
                path('<int:id>/edit/', views.transport_type_service_edit_admin,
                     name='transports-type-services-edit-admin'),
                path('<int:id>/delete/', views.transport_type_service_delete_admin,
                     name='transports-type-services-delete-admin'),
            ])),
            path('schedule-admin/', include([
                path('', views.transport_schedule_index_admin, name='transports-schedules-index-admin'),
                path('<int:id>/', views.transport_schedule_show_admin, name='transports-schedules-show-admin'),
                path('new/', views.transport_schedule_new_admin, name='transports-schedules-new-admin'),
                path('<int:id>/edit/', views.transport_schedule_edit_admin, name='transports-schedules-edit-admin'),
                path('<int:id>/delete/', views.transport_schedule_delete_admin,
                     name='transports-schedules-delete-admin'),
            ])),
        ])),
    ])),

    path('tourism_sites/', include([
        path('', views.tourism_site_index, name='tourism_sites-index'),
        path('<int:id>/', views.tourism_site_show, name='tourism_sites-show'),
        path('sites-admin/', include([
            path('', views.tourism_site_index_admin, name='tourism_sites-index-admin'),
            path('<int:id>/', views.tourism_site_show_admin, name='tourism_sites-show-admin'),
            path('new/', views.tourism_site_new_admin, name='tourism_sites-new-admin'),
            path('<int:id>/edit/', views.tourism_site_edit_admin, name='tourism_sites-edit-admin'),
            path('<int:id>/delete/', views.tourism_site_delete_admin, name='tourism_sites-delete-admin'),
            path('<int:id>/active/', views.tourism_site_active_admin, name='tourism_sites-active-admin'),
            path('<int:id>/inactive/', views.tourism_site_inactive_admin, name='tourism_sites-inactive-admin'),

            path('type-admin/', include([
                path('', views.tourism_site_type_index_admin, name='tourism_sites-types-index-admin'),
                path('<int:id>/', views.tourism_site_type_show_admin, name='tourism_sites-types-show-admin'),
                path('new/', views.tourism_site_type_new_admin, name='tourism_sites-types-new-admin'),
                path('<int:id>/edit/', views.tourism_site_type_edit_admin, name='tourism_sites-types-edit-admin'),
                path('<int:id>/delete/', views.tourism_site_type_delete_admin, name='tourism_sites-types-delete-admin'),
            ])),
            path('service-admin/', include([
                path('', views.tourism_site_service_index_admin, name='tourism_sites-services-index-admin'),
                path('<int:id>/', views.tourism_site_service_show_admin, name='tourism_sites-services-show-admin'),
                path('new/', views.tourism_site_service_new_admin, name='tourism_sites-services-new-admin'),
                path('<int:id>/edit/', views.tourism_site_service_edit_admin, name='tourism_sites-services-edit-admin'),
                path('<int:id>/delete/', views.tourism_site_service_delete_admin,
                     name='tourism_sites-services-delete-admin'),
            ])),
            path('menu-admin/', include([
                path('', views.tourism_site_menu_index_admin, name='tourism_sites-menus-index-admin'),
                path('<int:id>/', views.tourism_site_menu_show_admin, name='tourism_sites-menus-show-admin'),
                path('new/', views.tourism_site_menu_new_admin, name='tourism_sites-menus-new-admin'),
                path('<int:id>/edit/', views.tourism_site_menu_edit_admin, name='tourism_sites-menus-edit-admin'),
                path('<int:id>/delete/', views.tourism_site_menu_delete_admin, name='tourism_sites-menus-delete-admin'),
            ])),
            path('schedule-admin/', include([
                path('', views.tourism_site_schedule_index_admin, name='tourism_sites-schedules-index-admin'),
                path('<int:id>/', views.tourism_site_schedule_show_admin, name='tourism_sites-schedules-show-admin'),
                path('new/', views.tourism_site_schedule_new_admin, name='tourism_sites-schedules-new-admin'),
                path('<int:id>/edit/', views.tourism_site_schedule_edit_admin,
                     name='tourism_sites-schedules-edit-admin'),
                path('<int:id>/delete/', views.tourism_site_schedule_delete_admin,
                     name='tourism_sites-schedules-delete-admin'),
            ])),
        ])),
    ])),

    path('tourism_routes/', include([
        path('', views.tourism_route_index, name='tourism_routes-index'),
        path('<int:id>/', views.tourism_route_show, name='tourism_routes-show'),
        path('routes-admin/', include([
            path('', views.tourism_route_index_admin, name='tourism_routes-index-admin'),
            path('<int:id>/', views.tourism_route_show_admin, name='tourism_routes-show-admin'),
            path('new/', views.tourism_route_new_admin, name='tourism_routes-new-admin'),
            path('<int:id>/edit/', views.tourism_route_edit_admin, name='tourism_routes-edit-admin'),
            path('<int:id>/delete/', views.tourism_route_delete_admin, name='tourism_routes-delete-admin'),
            path('<int:id>/active/', views.tourism_route_active_admin, name='tourism_routes-active-admin'),
            path('<int:id>/inactive/', views.tourism_route_inactive_admin, name='tourism_routes-inactive-admin'),

            path('menu-admin/', include([
                path('', views.tourism_route_menu_index_admin, name='tourism_routes-menus-index-admin'),
                path('<int:id>/', views.tourism_route_menu_show_admin, name='tourism_routes-menus-show-admin'),
                path('new/', views.tourism_route_menu_new_admin, name='tourism_routes-menus-new-admin'),
                path('<int:id>/edit/', views.tourism_route_menu_edit_admin, name='tourism_routes-menus-edit-admin'),
                path('<int:id>/delete/', views.tourism_route_menu_delete_admin,
                     name='tourism_routes-menus-delete-admin'),
            ])),
        ])),
    ])),

    path('lodgings/', include([
        path('', views.lodging_index, name='lodging-index'),
        path('<int:id>/', views.lodging_show, name='lodging-show'),
        path('admin-lodgings/', include([
            path('', views.lodging_index_admin, name='lodgings-index-admin'),
            path('<int:id>/', views.lodging_show_admin, name='lodgings-show-admin'),
            path('new/', views.lodging_new_admin, name='lodgings-new-admin'),
            path('<int:id>/edit/', views.lodging_edit_admin, name='lodgings-edit-admin'),
            path('<int:id>/delete/', views.lodging_delete_admin, name='lodgings-delete-admin'),
            path('<int:id>/active/', views.lodging_active_admin, name='lodgings-active-admin'),
            path('<int:id>/inactive/', views.lodging_inactive_admin, name='lodgings-inactive-admin'),

            path('service-admin/', include([
                path('', views.lodging_service_index_admin, name='lodgings-services-index-admin'),
                path('<int:id>/', views.lodging_service_show_admin, name='lodgings-services-show-admin'),
                path('new/', views.lodging_service_new_admin, name='lodgings-services-new-admin'),
                path('<int:id>/edit/', views.lodging_service_edit_admin, name='lodgings-services-edit-admin'),
                path('<int:id>/delete/', views.lodging_service_delete_admin, name='lodgings-services-delete-admin'),
            ])),
            path('type-admin/', include([
                path('', views.lodging_type_index_admin, name='lodgings-types-index-admin'),
                path('<int:id>/', views.lodging_type_show_admin, name='lodgings-types-show-admin'),
                path('new/', views.lodging_type_new_admin, name='lodgings-types-new-admin'),
                path('<int:id>/edit/', views.lodging_type_edit_admin, name='lodgings-types-edit-admin'),
                path('<int:id>/delete/', views.lodging_type_delete_admin, name='lodgings-types-delete-admin'),
            ])),
            path('room-admin/', include([
                path('', views.lodging_room_index_admin, name='lodgings-room-index-admin'),
                path('<int:id>/', views.lodging_room_show_admin, name='lodgings-room-show-admin'),
                path('new/', views.lodging_room_new_admin, name='lodgings-room-new-admin'),
                path('<int:id>/edit/', views.lodging_room_edit_admin, name='lodgings-room-edit-admin'),
                path('<int:id>/delete/', views.lodging_room_delete_admin, name='lodgings-room-delete-admin'),
            ])),
            path('schedule-admin/', include([
                path('', views.lodging_schedule_index_admin, name='lodgings-schedules-index-admin'),
                path('<int:id>/', views.lodging_schedule_show_admin, name='lodgings-schedules-show-admin'),
                path('new/', views.lodging_schedule_new_admin, name='lodgings-schedules-new-admin'),
                path('<int:id>/edit/', views.lodging_schedule_edit_admin, name='lodgings-schedules-edit-admin'),
                path('<int:id>/delete/', views.lodging_schedule_delete_admin, name='lodgings-schedules-delete-admin'),
            ])),
        ])),

    ])),
]
