path('new/', views.assignment_site_new, name='assignment_sites-new-admin'),
path('<int:id>/edit/', views.assignment_site_edit, name='assignment_sites-edit-admin'),
path('<int:id>/delete/', views.assignment_site_delete, name='assignment_sites-delete-admin'),

path('new/', views.assignment_transport_new, name='assignment_transports-new-admin'),
path('<int:id>/edit/', views.assignment_transport_edit, name='assignment_transports-edit-admin'),
path('<int:id>/delete/', views.assignment_transport_delete, name='assignment_transports-delete-admin'),

path('new/', views.assignment_agency_new, name='assignment_agencies-new-admin'),
path('<int:id>/edit/', views.assignment_agency_edit, name='assignment_agencies-edit-admin'),
path('<int:id>/delete/', views.assignment_agency_delete, name='assignment_agencies-delete-admin'),

path('new/', views.assignment_restaurant_new, name='assignment_restaurants-new-admin'),
path('<int:id>/edit/', views.assignment_restaurant_edit, name='assignment_restaurants-edit-admin'),
path('<int:id>/delete/', views.assignment_restaurant_delete, name='assignment_restaurants-delete-admin'),

path('new/', views.assignment_lodging_new, name='assignment_lodgings-new-admin'),
path('<int:id>/edit/', views.assignment_lodging_edit, name='assignment_lodgings-edit-admin'),
path('<int:id>/delete/', views.assignment_lodging_delete, name='assignment_lodgings-delete-admin'),
