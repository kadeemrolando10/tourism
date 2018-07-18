from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

from tour.models import Event, Restaurant, TourismSite, Transport, Lodging, Agency, Objective, Function, \
    TransportDestination, LodgingRoom, LodgingType, TourismSiteDestiny, LodgingSchedule, TourismRouteDestiny, \
    TourismRoute, TourismSiteSchedule, TransportSchedule, RestaurantSchedule, LodgingService, AgencyService, \
    AgencySchedule, RestaurantService, RestaurantMenu, TransportService, TransportTypeService, TourismSiteMenu, \
    TourismSiteType, TourismSiteService, TourismRouteMenu, Law

from tour.forms import RestaurantForm, AgencyForm, EventForm, TransportForm, TourismSiteForm, TourismRouteForm, \
    LodgingForm, AgencyServiceForm, AgencyScheduleForm, RestaurantMenuForm, RestaurantScheduleForm, \
    RestaurantServiceForm, TransportDestinationForm, TransportServiceForm, TransportTypeServiceForm, \
    TransportScheduleForm, TourismSiteMenuForm, TourismSiteScheduleForm, TourismSiteDestinyForm, TourismSiteTypeForm, \
    TourismSiteServiceForm, TourismRouteMenuForm, TourismRouteDestinyForm, LodgingRoomForm, LodgingScheduleForm, \
    LodgingTypeForm, LodgingServiceForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/books/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    })


def users_index(request):
    users = User.objects.all
    return render(request, 'registration/users_index.html', {
        'users': users,
    })


def index_admin(request):
    return render(request, 'admin_page/index.html', {})


def index(request):
    events = Event.objects.all
    restaurants = Restaurant.objects.all
    transports = Transport.objects.all
    tourism_sites = Restaurant.objects.all
    agencys = Agency.objects.all
    lodgings = Lodging.objects.all
    return render(request, 'tour/index.html', {
        'events': events,
        'restaurants': restaurants,
        'transports': transports,
        'tourism_sites': tourism_sites,
        'agencys': agencys,
        'lodgings': lodgings,
    })


def secretary(request):
    obj = Objective.objects.all
    func = Function.objects.all
    doc = Law.objects.all
    return render(request, 'tour/secretary.html', {
        'objetivos': obj,
        'funciones': func,
        'documento': doc
    })


# AGENCIAS DE TURISMO CLIENTE


def agency_index(request):
    agencies = Agency.objects.all
    return render(request, 'tour/agencies-index.html', {
        'agencies': agencies,
        'agency_obj': Agency,
    })


def agency_show(request, id):
    agency = Agency.objects.get(id=id)
    services = AgencyService.objects.filter(agency=id)
    schedule = AgencySchedule.objects.filter(agency=id)
    return render(request, 'tour/agencies-show.html', {
        'agency': agency,
        'agency_obj': Agency,
        'services': services,
        'schedule': schedule
    })


# AGENCIAS DE TURISMO ADMINISTRADOR


def agency_index_admin(request):
    agencies = Agency.objects.all
    return render(request, 'admin_page/agencies/index.html', {
        'agencies': agencies,
        'agency_obj': Agency,
    })


def agency_show_admin(request, id):
    agency = Agency.objects.get(id=id)
    request.session['agency'] = id
    return render(request, 'admin_page/agencies/show.html', {
        'agency': agency,
        'agency_obj': Agency,
    })


def agency_new_admin(request):
    if request.method == 'POST':
        form = AgencyForm(request.POST, request.FILES)
        if form.is_valid():
            agency = form.save(commit=False)
            agency.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse(agency_index_admin))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = AgencyForm()
    return render(request, 'admin_page/agencies/new.html', {
        'form': form,
    })


def agency_edit_admin(request, id):
    agency = Agency.objects.get(id=id)
    if request.method == 'POST':
        form = AgencyForm(request.POST, request.FILES, instance=agency)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('agencies-show-admin', kwargs={'id': agency.id}))
    else:
        form = AgencyForm(instance=agency)
    return render(request, 'admin_page/agencies/edit.html', {
        'agency': agency,
        'form': form,
        'agency_obj': Agency
    })


def agency_delete_admin(request, id):
    agency = Agency.objects.get(id=id)
    agency.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(agency_index_admin))


# SERVICIOS DE AGENCIAS

def agency_service_index_admin(request):
    agency = request.session['agency']
    services = AgencyService.objects.filter(agency=agency)
    agency_title = Agency.objects.get(id=agency)
    agency_id = agency
    return render(request, 'admin_page/agencies/services/index.html', {
        'services': services,
        'service_obj': AgencyService,
        'agency_title': agency_title,
        'agency_id': agency_id
    })


def agency_service_show_admin(request, id):
    agency = request.session['agency']
    service = AgencyService.objects.filter(agency=agency).get(id=id)
    agency_title = Agency.objects.get(id=agency)
    return render(request, 'admin_page/agencies/services/show.html', {
        'service': service,
        'service_obj': AgencyService,
        'agency_title': agency_title
    })


def agency_service_new_admin(request):
    agency = request.session['agency']
    agency_title = Agency.objects.get(id=agency)
    if request.method == 'POST':
        form = AgencyServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('agencies-services-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = AgencyServiceForm(initial={'agency': agency})
    return render(request, 'admin_page/agencies/services/new.html', {
        'form': form,
        'agency_title': agency_title
    })


def agency_service_edit_admin(request, id):
    agency = request.session['agency']
    service = AgencyService.objects.filter(agency=agency).get(id=id)
    agency_title = Agency.objects.get(id=agency)
    if request.method == 'POST':
        form = AgencyServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('agencies-services-show-admin', kwargs={'id': service.id}))
    else:
        form = AgencyServiceForm(instance=service)
    return render(request, 'admin_page/agencies/services/edit.html', {
        'service': service,
        'form': form,
        'service_obj': AgencyService,
        'agency_title': agency_title
    })


def agency_service_delete_admin(request, id):
    agency = request.session['agency']
    service = AgencyService.objects.filter(agency=agency).get(id=id)
    service.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('agencies-services-index-admin'))


# HORARIOS DE AGENCIA

def agency_schedule_index_admin(request):
    agency = request.session['agency']
    schedules = AgencySchedule.objects.filter(agency=agency)
    agency_title = Agency.objects.get(id=agency)
    agency_id = agency
    return render(request, 'admin_page/agencies/schedules/index.html', {
        'schedules': schedules,
        'schedule_obj': AgencySchedule,
        'agency_title': agency_title,
        'agency_id': agency_id
    })


def agency_schedule_show_admin(request, id):
    agency = request.session['agency']
    schedule = AgencySchedule.objects.filter(agency=agency).get(id=id)
    agency_title = Agency.objects.get(id=agency)
    return render(request, 'admin_page/agencies/schedules/show.html', {
        'schedule': schedule,
        'schedule_obj': AgencySchedule,
        'agency_title': agency_title
    })


def agency_schedule_new_admin(request):
    agency = request.session['agency']
    agency_title = Agency.objects.get(id=agency)
    if request.method == 'POST':
        form = AgencyScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('agencies-schedules-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = AgencyScheduleForm(initial={'agency': agency})
    return render(request, 'admin_page/agencies/schedules/new.html', {
        'form': form,
        'agency_title': agency_title
    })


def agency_schedule_edit_admin(request, id):
    agency = request.session['agency']
    schedule = AgencySchedule.objects.filter(agency=agency).get(id=id)
    agency_title = Agency.objects.get(id=agency)
    if request.method == 'POST':
        form = AgencyScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('agencies-schedules-show-admin', kwargs={'id': schedule.id}))
    else:
        form = AgencyScheduleForm(instance=schedule)
    return render(request, 'admin_page/agencies/schedules/edit.html', {
        'schedule': schedule,
        'form': form,
        'schedule_obj': AgencySchedule,
        'agency_title': agency_title
    })


def agency_schedule_delete_admin(request, id):
    agency = request.session['agency']
    schedule = AgencySchedule.objects.filter(agency=agency).get(id=id)
    schedule.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('agencies-schedules-index-admin'))


# EVENTOS CLIENTE

def event_index(request):
    events = Event.objects.all
    return render(request, 'tour/events-index.html', {
        'events': events,
        'event_obj': Event
    })


# EVENTOS ADMINISTRADOR

def event_index_admin(request):
    events = Event.objects.all
    return render(request, 'admin_page/events/index.html', {
        'events': events,
        'event_obj': Event
    })


def event_show_admin(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'admin_page/events/show.html', {
        'event': event,
        'event_obj': Event
    })


def event_new_admin(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse(event_index_admin))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = EventForm()
    return render(request, 'admin_page/events/new.html', {
        'form': form,
    })


def event_edit_admin(request, id):
    event = Event.objects.get(id=id)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('events-show-admin', kwargs={'id': event.id}))
    else:
        form = EventForm(instance=event)
    return render(request, 'admin_page/events/edit.html', {
        'event': event,
        'form': form,
        'event_obj': Event
    })


def event_delete_admin(request, id):
    event = Event.objects.get(id=id)
    event.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(event_index_admin))


# RESTAURANTS CLIENTE

def restaurant_index(request):
    restaurants = Restaurant.objects.all
    return render(request, 'tour/restaurants-index.html', {
        'restaurants': restaurants,
        'restaurant_obj': Restaurant
    })


def restaurant_show(request, id):
    restaurant = Restaurant.objects.get(id=id)
    menu = RestaurantMenu.objects.filter(restaurant=id).order_by('price')
    schedule = RestaurantSchedule.objects.filter(restaurant=id).order_by('published_date')
    return render(request, 'tour/restaurants-show.html', {
        'restaurant': restaurant,
        'restaurant_obj': Restaurant,
        'schedule': schedule,
        'menu': menu,
    })


# RESTAURANTS ADMINISTRADOR

def restaurant_index_admin(request):
    restaurants = Restaurant.objects.all
    return render(request, 'admin_page/restaurants/index.html', {
        'restaurants': restaurants,
        'restaurant_obj': Restaurant
    })


def restaurant_show_admin(request, id):
    request.session['restaurants'] = id
    restaurant = Restaurant.objects.get(id=id)
    return render(request, 'admin_page/restaurants/show.html', {
        'restaurant': restaurant,
        'restaurant_obj': Restaurant
    })


def restaurant_new_admin(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse(restaurant_index_admin))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = RestaurantForm()
    return render(request, 'admin_page/restaurants/new.html', {
        'form': form,
    })


def restaurant_edit_admin(request, id):
    restaurant = Restaurant.objects.get(id=id)

    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('restaurants-show-admin', kwargs={'id': restaurant.id}))
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'admin_page/restaurants/edit.html', {
        'restaurant': restaurant,
        'form': form,
        'restaurant_obj': Restaurant
    })


def restaurant_delete_admin(request, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.delete()
    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(restaurant_index_admin))


# MENU DE RESTAURANTES
def restaurant_menu_index_admin(request):
    restaurant = request.session['restaurants']
    menus = RestaurantMenu.objects.filter(restaurant=restaurant)
    restaurant_title = Restaurant.objects.get(id=restaurant)
    restaurant_id = restaurant
    return render(request, 'admin_page/restaurants/menus/index.html', {
        'menus': menus,
        'menu_obj': RestaurantMenu,
        'restaurant_title': restaurant_title,
        'restaurant_id': restaurant_id
    })


def restaurant_menu_show_admin(request, id):
    restaurant = request.session['restaurants']
    menu = RestaurantMenu.objects.filter(restaurant=restaurant).get(id=id)
    restaurant_title = Restaurant.objects.get(id=restaurant)
    return render(request, 'admin_page/restaurants/menus/show.html', {
        'menu': menu,
        'menu_obj': RestaurantMenu,
        'restaurant_title': restaurant_title
    })


def restaurant_menu_new_admin(request):
    restaurant = request.session['restaurants']
    restaurant_title = Restaurant.objects.get(id=restaurant)
    if request.method == 'POST':
        form = RestaurantMenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('restaurants-menus-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = RestaurantMenuForm(initial={'restaurant': restaurant})
    return render(request, 'admin_page/restaurants/menus/new.html', {
        'form': form,
        'restaurant_title': restaurant_title
    })


def restaurant_menu_edit_admin(request, id):
    restaurant = request.session['restaurants']
    menu = RestaurantMenu.objects.filter(restaurant=restaurant).get(id=id)
    restaurant_title = Restaurant.objects.get(id=restaurant)
    if request.method == 'POST':
        form = RestaurantMenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('restaurants-menus-index-admin'))
    else:
        form = RestaurantMenuForm(instance=menu)
    return render(request, 'admin_page/restaurants/menus/edit.html', {
        'menu': menu,
        'form': form,
        'menu_obj': RestaurantMenu,
        'restaurant_title': restaurant_title
    })


def restaurant_menu_delete_admin(request, id):
    restaurant = request.session['restaurants']
    menu = RestaurantMenu.objects.filter(restaurant=restaurant).get(id=id)
    menu.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('restaurants-menus-index-admin'))


# HORARIOS DE RESTAURANTES

def restaurant_schedule_index_admin(request):
    restaurant = request.session['restaurants']
    schedules = RestaurantSchedule.objects.filter(restaurant=restaurant)
    restaurant_title = Restaurant.objects.get(id=restaurant)
    restaurant_id = restaurant
    return render(request, 'admin_page/restaurants/schedules/index.html', {
        'schedules': schedules,
        'schedule_obj': RestaurantSchedule,
        'restaurant_title': restaurant_title,
        'restaurant_id': restaurant_id
    })


def restaurant_schedule_show_admin(request, id):
    restaurant = request.session['restaurants']
    schedule = RestaurantSchedule.objects.filter(restaurant=restaurant).get(id=id)
    restaurant_title = Restaurant.objects.get(id=restaurant)
    return render(request, 'admin_page/restaurants/schedules/show.html', {
        'schedule': schedule,
        'schedule_obj': RestaurantSchedule,
        'restaurant_title': restaurant_title
    })


def restaurant_schedule_new_admin(request):
    restaurant = request.session['restaurants']
    restaurant_title = Restaurant.objects.get(id=restaurant)
    if request.method == 'POST':
        form = RestaurantScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('restaurants-schedules-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = RestaurantScheduleForm(initial={'restaurant': restaurant})
    return render(request, 'admin_page/restaurants/schedules/new.html', {
        'form': form,
        'restaurant_title': restaurant_title
    })


def restaurant_schedule_edit_admin(request, id):
    restaurant = request.session['restaurants']
    schedule = RestaurantSchedule.objects.filter(restaurant=restaurant).get(id=id)
    restaurant_title = Restaurant.objects.get(id=restaurant)
    if request.method == 'POST':
        form = RestaurantScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('restaurants-schedules-index-admin'))
    else:
        form = RestaurantScheduleForm(instance=schedule)
    return render(request, 'admin_page/restaurants/schedules/edit.html', {
        'schedule': schedule,
        'form': form,
        'schedule_obj': RestaurantSchedule,
        'restaurant_title': restaurant_title
    })


def restaurant_schedule_delete_admin(request, id):
    restaurant = request.session['restaurants']
    schedule = RestaurantSchedule.objects.filter(restaurant=restaurant).get(id=id)
    schedule.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('restaurants-schedules-index-admin'))


# SERVICIOS DE RESTAURANTES

def restaurant_service_index_admin(request):
    services = RestaurantService.objects.all
    return render(request, 'admin_page/restaurants/services/index.html', {
        'services': services,
        'service_obj': RestaurantService,
    })


def restaurant_service_show_admin(request, id):
    service = RestaurantService.objects.get(id=id)
    return render(request, 'admin_page/restaurants/services/show.html', {
        'service': service,
        'service_obj': RestaurantService,
    })


def restaurant_service_new_admin(request):
    if request.method == 'POST':
        form = RestaurantServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('restaurants-services-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = RestaurantServiceForm()
    return render(request, 'admin_page/restaurants/services/new.html', {
        'form': form,
    })


def restaurant_service_edit_admin(request, id):
    service = RestaurantService.objects.get(id=id)
    if request.method == 'POST':
        form = RestaurantServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('restaurants-services-index-admin'))
    else:
        form = RestaurantServiceForm(instance=service)
    return render(request, 'admin_page/restaurants/services/edit.html', {
        'service': service,
        'form': form,
        'service_obj': RestaurantService
    })


def restaurant_service_delete_admin(request, id):
    service = RestaurantService.objects.get(id=id)
    service.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('restaurants-services-index-admin'))


# TRANSPORTES CLIENTE

def transport_index(request):
    transports = Transport.objects.all
    return render(request, 'tour/transports-index.html', {
        'transports': transports,
        'transport_obj': Transport
    })


def transport_show(request, id):
    transport = Transport.objects.get(id=id)
    schedule = TransportSchedule.objects.filter(transport=id).order_by('published_date')
    destinations = TransportDestination.objects.filter(transport__id=id)
    return render(request, 'tour/transports-show.html', {
        'transport': transport,
        'destinations': destinations,
        'schedule': schedule,
        'transport_obj': Transport
    })


# TRANSPORTES ADMINISTRADOR

def transport_index_admin(request):
    transports = Transport.objects.all
    return render(request, 'admin_page/transports/index.html', {
        'transports': transports,
        'transport_obj': Transport
    })


def transport_show_admin(request, id):
    transport = Transport.objects.get(id=id)
    request.session['transports'] = id
    destinations = TransportDestination.objects.filter(transport__id=id)
    return render(request, 'admin_page/transports/show.html', {
        'transport': transport,
        'destinations': destinations,
        'transport_obj': Transport
    })


def transport_new_admin(request):
    if request.method == 'POST':
        form = TransportForm(request.POST, request.FILES)
        if form.is_valid():
            transport = form.save(commit=False)
            transport.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse(transport_index_admin))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TransportForm()
    return render(request, 'admin_page/transports/new.html', {
        'form': form,
    })


def transport_edit_admin(request, id):
    transport = Transport.objects.get(id=id)

    if request.method == 'POST':
        form = TransportForm(request.POST, request.FILES, instance=transport)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('transports-show-admin', kwargs={'id': transport.id}))
    else:
        form = TransportForm(instance=transport)
    return render(request, 'admin_page/transports/edit.html', {
        'transports': transport,
        'form': form,
        'transport_obj': Transport
    })


def transport_delete_admin(request, id):
    transport = Transport.objects.get(id=id)
    transport.delete()
    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(transport_index_admin))


# DESTINOS DE TRANSPORTES
def transport_destination_index_admin(request):
    transport = request.session['transports']
    destinations = TransportDestination.objects.filter(transport=transport)
    transport_title = Transport.objects.get(id=transport)
    transport_id = transport

    return render(request, 'admin_page/transports/destinations/index.html', {
        'destinations': destinations,
        'destination_obj': TransportDestination,
        'transport_title': transport_title,
        'transport_id': transport_id
    })


def transport_destination_show_admin(request, id):
    transport = request.session['transports']
    destination = TransportDestination.objects.filter(transport=transport).get(id=id)
    transport_title = Transport.objects.get(id=transport)
    request.session['destination'] = id
    return render(request, 'admin_page/transports/destinations/show.html', {
        'destination': destination,
        'destination_obj': TransportDestination,
        'transport_title': transport_title
    })


def transport_destination_new_admin(request):
    transport = request.session['transports']
    transport_title = Transport.objects.get(id=transport)
    if request.method == 'POST':
        form = TransportDestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('transports-destination-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TransportDestinationForm(initial={'transport': transport})
    return render(request, 'admin_page/transports/destinations/new.html', {
        'form': form,
        'transport_title': transport_title
    })


def transport_destination_edit_admin(request, id):
    transport = request.session['transports']
    destination = TransportDestination.objects.filter(transport=transport).get(id=id)
    transport_title = Transport.objects.get(id=transport)
    if request.method == 'POST':
        form = TransportDestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('transports-destination-index-admin'))
    else:
        form = TransportDestinationForm(instance=destination)
    return render(request, 'admin_page/transports/destinations/edit.html', {
        'destination': destination,
        'form': form,
        'destination_obj': TransportDestination,
        'transport_title': transport_title
    })


def transport_destination_delete_admin(request, id):
    transport = request.session['transports']
    destination = TransportDestination.objects.filter(transport=transport).get(id=id)
    destination.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('transports-destination-index-admin'))


# SERVICIO DE TRANSPORTES
def transport_service_index_admin(request):
    services = TransportService.objects.all
    return render(request, 'admin_page/transports/services/index.html', {
        'services': services,
        'service_obj': TransportService,
    })


def transport_service_show_admin(request, id):
    service = TransportService.objects.get(id=id)
    return render(request, 'admin_page/transports/services/show.html', {
        'service': service,
        'service_obj': TransportService,
    })


def transport_service_new_admin(request):
    if request.method == 'POST':
        form = TransportServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('transports-services-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TransportServiceForm()
    return render(request, 'admin_page/transports/services/new.html', {
        'form': form,
    })


def transport_service_edit_admin(request, id):
    service = TransportService.objects.get(id=id)
    if request.method == 'POST':
        form = TransportServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('transports-services-index-admin'))
    else:
        form = TransportServiceForm(instance=service)
    return render(request, 'admin_page/transports/services/edit.html', {
        'service': service,
        'form': form,
        'service_obj': TransportService,
    })


def transport_service_delete_admin(request, id):
    service = TransportService.objects.get(id=id)
    service.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('transports-services-index-admin'))


# TIPO DE SERVICIO DE TRANSPORTES

def transport_type_service_index_admin(request):
    transport = request.session['transports']
    destination = request.session['destination']
    type_services = TransportTypeService.objects.filter(destination=destination)
    transport_title = Transport.objects.get(id=transport)
    destination_title = TransportDestination.objects.get(id=destination)
    destination_id = destination
    return render(request, 'admin_page/transports/type_services/index.html', {
        'type_services': type_services,
        'type_service_obj': TransportTypeService,
        'transport_title': transport_title,
        'destination_title': destination_title,
        'destination_id': destination_id
    })


def transport_type_service_show_admin(request, id):
    transport = request.session['transports']
    destination = request.session['destination']
    type_service = TransportTypeService.objects.filter(destination=destination)
    transport_title = Transport.objects.get(id=transport)
    destination_title = TransportDestination.objects.get(id=destination)
    return render(request, 'admin_page/transports/type_services/show.html', {
        'type_service': type_service,
        'type_service_obj': TransportTypeService,
        'transport_title': transport_title,
        'destination_title': destination_title
    })


def transport_type_service_new_admin(request):
    transport = request.session['transports']
    destination = request.session['destination']
    transport_title = Transport.objects.get(id=transport)
    destination_title = TransportDestination.objects.get(id=destination)
    if request.method == 'POST':
        form = TransportTypeServiceForm(request.POST, request.FILES)
        if form.is_valid():
            type_service = form.save(commit=False)
            type_service.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('transports-type-services-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TransportTypeServiceForm(initial={'destination': destination})
    return render(request, 'admin_page/transports/type_services/new.html', {
        'form': form,
        'transport_title': transport_title,
        'destination_title': destination_title
    })


def transport_type_service_edit_admin(request, id):
    transport = request.session['transports']
    destination = request.session['destination']
    type_service = TransportTypeService.objects.get(destination=destination)
    transport_title = Transport.objects.get(id=transport)
    destination_title = TransportDestination.objects.get(id=destination)
    if request.method == 'POST':
        form = TransportTypeServiceForm(request.POST, request.FILES, instance=type_service)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('transports-type-services-index-admin'))
    else:
        form = TransportTypeServiceForm(instance=type_service)
    return render(request, 'admin_page/transports/type_services/edit.html', {
        'type_service': type_service,
        'form': form,
        'type_service_obj': TransportTypeService,
        'transport_title': transport_title,
        'destination_title': destination_title
    })


def transport_type_service_delete_admin(request, id):
    destination = request.session['destination']
    type_service = TransportTypeService.objects.filter(destination=destination)
    type_service.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('transports-type-services-index-admin'))


# HORARIOS DE TRANSPORTES

def transport_schedule_index_admin(request):
    transport = request.session['transports']
    schedules = TransportSchedule.objects.filter(transport=transport)
    transport_title = Transport.objects.get(id=transport)
    transport_id = transport
    return render(request, 'admin_page/transports/schedules/index.html', {
        'schedules': schedules,
        'schedule_obj': TransportSchedule,
        'transport_title': transport_title,
        'transport_id': transport_id
    })


def transport_schedule_show_admin(request, id):
    transport = request.session['transports']
    schedule = TransportSchedule.objects.filter(transport=transport).get(id=id)
    transport_title = Transport.objects.get(id=transport)
    return render(request, 'admin_page/transports/schedules/show.html', {
        'schedule': schedule,
        'schedule_obj': TransportSchedule,
        'transport_title': transport_title
    })


def transport_schedule_new_admin(request):
    transport = request.session['transports']
    transport_title = Transport.objects.get(id=transport)
    if request.method == 'POST':
        form = TransportScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('transports-schedules-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TransportScheduleForm(initial={'transport': transport})
    return render(request, 'admin_page/transports/schedules/new.html', {
        'form': form,
        'transport_title': transport_title
    })


def transport_schedule_edit_admin(request, id):
    transport = request.session['transports']
    schedule = TransportSchedule.objects.filter(transport=transport).get(id=id)
    transport_title = Transport.objects.get(id=transport)
    if request.method == 'POST':
        form = TransportScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('transports-schedules-index-admin'))
    else:
        form = TransportScheduleForm(instance=schedule)
    return render(request, 'admin_page/transports/schedules/edit.html', {
        'schedule': schedule,
        'form': form,
        'schedule_obj': TransportSchedule,
        'transport_title': transport_title
    })


def transport_schedule_delete_admin(request, id):
    transport = request.session['transports']
    schedule = TransportSchedule.objects.filter(transport=transport).get(id=id)
    schedule.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('transports-schedules-index-admin'))


# SITIOS TURISTICOS CLIENTE

def tourism_site_index(request):
    destiny = TourismSiteDestiny.objects.all
    return render(request, 'tour/tourism_sites-index.html', {
        'destiny': destiny,
        'tourism_site_obj': TourismSite
    })


def tourism_site_show(request, id):
    site = TourismSite.objects.get(id=id)
    schedule = TourismSiteSchedule.objects.filter(site=id).order_by('published_date')
    return render(request, 'tour/tourism_site-show.html', {
        'site': site,
        'schedule': schedule,
    })


# DESTINOS DE SITIOS TURISTICOS

def tourism_site_destination_index_admin(request):
    destinations = TourismSiteDestiny.objects.all
    return render(request, 'admin_page/tourism_sites/destinations/index.html', {
        'destinations': destinations,
        'destination_obj': TourismSiteDestiny,
    })


def tourism_site_destination_show_admin(request, id):
    destination = TourismSiteDestiny.objects.get(id=id)
    request.session['destiny_tourism_site'] = id
    return render(request, 'admin_page/tourism_sites/destinations/show.html', {
        'destination': destination,
        'destination_obj': TourismSiteDestiny,
    })


def tourism_site_destination_new_admin(request):
    if request.method == 'POST':
        form = TourismSiteDestinyForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('tourism_sites-destination-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TourismSiteDestinyForm()
    return render(request, 'admin_page/tourism_sites/destinations/new.html', {
        'form': form,
    })


def tourism_site_destination_edit_admin(request, id):
    destination = TourismSiteDestiny.objects.get(id=id)
    if request.method == 'POST':
        form = TourismSiteDestinyForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('tourism_sites-destination-index-admin'))
    else:
        form = TourismSiteDestinyForm(instance=destination)
    return render(request, 'admin_page/tourism_sites/destinations/edit.html', {
        'destination': destination,
        'form': form,
        'destination_obj': TourismSiteDestiny
    })


def tourism_site_destination_delete_admin(request, id):
    destination = TourismSiteDestiny.objects.get(id=id)
    destination.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('tourism_sites-destination-index-admin'))


# SITIOS TURISTICOS ADMINISTRADOR

def tourism_site_index_admin(request):
    destiny = request.session['destiny_tourism_site']
    sites = TourismSite.objects.filter(destination=destiny)
    destiny_title = TourismSiteDestiny.objects.get(id=destiny)
    destiny_id = destiny
    return render(request, 'admin_page/tourism_sites/index.html', {
        'sites': sites,
        'site_obj': TourismSite,
        'destiny_title': destiny_title,
        'destiny_id': destiny_id,
    })


def tourism_site_show_admin(request, id):
    destiny = request.session['destiny_tourism_site']
    site = TourismSite.objects.filter(destination=destiny).get(id=id)
    destiny_title = TourismSiteDestiny.objects.get(id=destiny)
    request.session['tourism_site'] = id
    return render(request, 'admin_page/tourism_sites/show.html', {
        'site': site,
        'site_obj': TourismSite,
        'destiny_title': destiny_title,
    })


def tourism_site_new_admin(request):
    destiny = request.session['destiny_tourism_site']
    destiny_title = TourismSiteDestiny.objects.get(id=destiny)
    if request.method == 'POST':
        form = TourismSiteForm(request.POST, request.FILES)
        if form.is_valid():
            tourism_site = form.save(commit=False)
            tourism_site.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse(tourism_site_index_admin))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TourismSiteForm(initial={'destination': destiny})
    return render(request, 'admin_page/tourism_sites/new.html', {
        'form': form,
        'destiny_title': destiny_title,
    })


def tourism_site_edit_admin(request, id):
    destiny = request.session['destiny_tourism_site']
    destiny_title = TourismSiteDestiny.objects.get(id=destiny)
    tourism_site = TourismSite.objects.filter(destination=destiny).get(id=id)

    if request.method == 'POST':
        form = TourismSiteForm(request.POST, request.FILES, instance=tourism_site)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('tourism_sites-show-admin', kwargs={'id': tourism_site.id}))
    else:
        form = TourismSiteForm(instance=tourism_site)
    return render(request, 'admin_page/tourism_sites/edit.html', {
        'tourism_site': tourism_site,
        'form': form,
        'tourism_site_obj': TourismSite,
        'destiny_title': destiny_title,
    })


def tourism_site_delete_admin(request, id):
    tourism_site = TourismSite.objects.get(id=id)
    tourism_site.delete()
    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(tourism_site_index_admin))


# MENU DE SITIOS TURISTICOS

def tourism_site_menu_index_admin(request):
    destiny = request.session['destiny_tourism_site']
    tourism_site = request.session['tourism_site']
    menus = TourismSiteMenu.objects.filter(site=tourism_site)
    site_title = TourismSite.objects.get(id=tourism_site)
    site_id = tourism_site
    destiny_title = TourismSiteDestiny.objects.get(id=destiny)
    return render(request, 'admin_page/tourism_sites/menus/index.html', {
        'menus': menus,
        'menu_obj': TourismSiteMenu,
        'site_title': site_title,
        'site_id': site_id,
        'destiny_title': destiny_title,
    })


def tourism_site_menu_show_admin(request, id):
    tourism_site = request.session['tourism_site']
    menu = TourismSiteMenu.objects.filter(site=tourism_site).get(id=id)
    tourism_site_title = TourismSite.objects.get(id=tourism_site)
    return render(request, 'admin_page/tourism_sites/menus/show.html', {
        'menu': menu,
        'menu_obj': TourismSiteMenu,
        'tourism_site_title': tourism_site_title
    })


def tourism_site_menu_new_admin(request):
    tourism_site = request.session['tourism_site']
    destiny = request.session['destiny_tourism_site']
    site_title = TourismSite.objects.get(id=tourism_site)
    destiny_title = TourismSiteDestiny.objects.get(id=destiny)
    if request.method == 'POST':
        form = TourismSiteMenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('tourism_sites-menus-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TourismSiteMenuForm(initial={'site': tourism_site})
    return render(request, 'admin_page/tourism_sites/menus/new.html', {
        'form': form,
        'site_title': site_title,
        'destiny_title': destiny_title,
    })


def tourism_site_menu_edit_admin(request, id):
    tourism_site = request.session['tourism_site']
    menu = TourismSiteMenu.objects.filter(site=tourism_site).get(id=id)
    site_title = TourismSite.objects.get(id=tourism_site)
    destiny = request.session['destiny_tourism_site']
    destiny_title = TourismSiteDestiny.objects.get(id=destiny)
    if request.method == 'POST':
        form = TourismSiteMenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('tourism_sites-menus-index-admin'))
    else:
        form = TourismSiteMenuForm(instance=menu)
    return render(request, 'admin_page/tourism_sites/menus/edit.html', {
        'menu': menu,
        'form': form,
        'menu_obj': TourismSiteMenu,
        'site_title': site_title,
        'destiny_title': destiny_title,
    })


def tourism_site_menu_delete_admin(request, id):
    tourism_site = request.session['tourism_site']
    menu = TourismSiteMenu.objects.filter(site=tourism_site).get(id=id)
    menu.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('tourism_sites-menus-index-admin'))


# HORARIOS DE SITIOS TURISTICOS

def tourism_site_schedule_index_admin(request):
    tourism_site = request.session['tourism_site']
    schedules = TourismSiteSchedule.objects.filter(site=tourism_site)
    site_title = TourismSite.objects.get(id=tourism_site)
    destiny = request.session['destiny_tourism_site']
    destiny_title = TourismSiteDestiny.objects.get(id=destiny)
    return render(request, 'admin_page/tourism_sites/schedules/index.html', {
        'schedules': schedules,
        'schedule_obj': TourismSiteSchedule,
        'site_title': site_title,
        'destiny_title': destiny_title,
    })


def tourism_site_schedule_show_admin(request, id):
    tourism_site = request.session['tourism_site']
    schedule = TourismSiteSchedule.objects.filter(tourism_site=tourism_site).get(id=id)
    tourism_site_title = TourismSite.objects.get(id=tourism_site)
    return render(request, 'admin_page/tourism_sites/schedules/show.html', {
        'schedule': schedule,
        'schedule_obj': TourismSiteSchedule,
        'tourism_site_title': tourism_site_title
    })


def tourism_site_schedule_new_admin(request):
    tourism_site = request.session['tourism_site']
    site_title = TourismSite.objects.get(id=tourism_site)
    destiny = request.session['destiny_tourism_site']
    destiny_title = TourismSiteDestiny.objects.get(id=destiny)
    if request.method == 'POST':
        form = TourismSiteScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('tourism_sites-schedules-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TourismSiteScheduleForm(initial={'site': tourism_site})
    return render(request, 'admin_page/tourism_sites/schedules/new.html', {
        'form': form,
        'site_title': site_title,
        'destiny_title': destiny_title,
    })


def tourism_site_schedule_edit_admin(request, id):
    tourism_site = request.session['tourism_site']
    schedule = TourismSiteSchedule.objects.filter(site=tourism_site).get(id=id)
    site_title = TourismSite.objects.get(id=tourism_site)
    destiny = request.session['destiny_tourism_site']
    destiny_title = TourismSiteDestiny.objects.get(id=destiny)
    if request.method == 'POST':
        form = TourismSiteScheduleForm(request.POST, request.FILES, instance=schedule)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('tourism_sites-schedules-index-admin'))
    else:
        form = TourismSiteScheduleForm(instance=schedule)
    return render(request, 'admin_page/tourism_sites/schedules/edit.html', {
        'schedule': schedule,
        'form': form,
        'schedule_obj': TourismSiteSchedule,
        'site_title': site_title,
        'destiny_title': destiny_title,
    })


def tourism_site_schedule_delete_admin(request, id):
    tourism_site = request.session['tourism_site']
    schedule = TourismSiteSchedule.objects.filter(site=tourism_site).get(id=id)
    schedule.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('tourism_sites-schedules-index-admin'))


# TIPOS DE SITIOS TURISTICOS

def tourism_site_type_index_admin(request):
    types = TourismSiteType.objects.all
    return render(request, 'admin_page/tourism_sites/types/index.html', {
        'types': types,
        'type_obj': TourismSiteType,
    })


def tourism_site_type_show_admin(request, id):
    type = TourismSiteType.objects.get(id=id)
    return render(request, 'admin_page/tourism_sites/types/show.html', {
        'type': type,
        'type_obj': TourismSiteType,
    })


def tourism_site_type_new_admin(request):
    if request.method == 'POST':
        form = TourismSiteTypeForm(request.POST, request.FILES)
        if form.is_valid():
            type = form.save(commit=False)
            type.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('tourism_sites-types-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TourismSiteTypeForm()
    return render(request, 'admin_page/tourism_sites/types/new.html', {
        'form': form,
    })


def tourism_site_type_edit_admin(request, id):
    type = TourismSiteType.objects.get(id=id)
    if request.method == 'POST':
        form = TourismSiteTypeForm(request.POST, request.FILES, instance=type)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('tourism_sites-types-index-admin'))
    else:
        form = TourismSiteTypeForm(instance=type)
    return render(request, 'admin_page/tourism_sites/types/edit.html', {
        'type': type,
        'form': form,
        'type_obj': TourismSiteType
    })


def tourism_site_type_delete_admin(request, id):
    type = TourismSiteType.objects.get(id=id)
    type.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('tourism_sites-types-index-admin'))


# SERVICIOS DE SITIOS TURISTICOS

def tourism_site_service_index_admin(request):
    services = TourismSiteService.objects.all
    return render(request, 'admin_page/tourism_sites/services/index.html', {
        'services': services,
        'service_obj': TourismSiteService,
    })


def tourism_site_service_show_admin(request, id):
    service = TourismSiteService.objects.get(id=id)
    return render(request, 'admin_page/tourism_sites/services/show.html', {
        'service': service,
        'service_obj': TourismSiteService,
    })


def tourism_site_service_new_admin(request):
    if request.method == 'POST':
        form = TourismSiteServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('tourism_sites-services-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TourismSiteServiceForm()
    return render(request, 'admin_page/tourism_sites/services/new.html', {
        'form': form,
    })


def tourism_site_service_edit_admin(request, id):
    service = TourismSiteService.objects.get(id=id)
    if request.method == 'POST':
        form = TourismSiteServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('tourism_sites-services-index-admin'))
    else:
        form = TourismSiteServiceForm(instance=service)
    return render(request, 'admin_page/tourism_sites/services/edit.html', {
        'service': service,
        'form': form,
        'service_obj': TourismSiteService
    })


def tourism_site_service_delete_admin(request, id):
    service = TourismSiteService.objects.get(id=id)
    service.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('tourism_sites-services-index-admin'))


# RUTAS TURISTICAS CLIENTE

def tourism_route_index(request):
    destiny = TourismRouteDestiny.objects.all
    return render(request, 'tour/tourism_route-index.html', {
        'destiny': destiny,
        'tourism_route_obj': TourismRoute
    })


def tourism_route_show(request, id):
    route = TourismRoute.objects.get(id=id)
    return render(request, 'tour/tourism_route-show.html', {
        'route': route,

    })


# DESTINOS DE RUTAS TURISTICAS

def tourism_route_destination_index_admin(request):
    destinations = TourismRouteDestiny.objects.all
    return render(request, 'admin_page/tourism_routes/destinations/index.html', {
        'destinations': destinations,
        'destination_obj': TourismRouteDestiny,
    })


def tourism_route_destination_show_admin(request, id):
    destination = TourismRouteDestiny.objects.get(id=id)
    request.session['destiny_tourism_route'] = id
    return render(request, 'admin_page/tourism_routes/destinations/show.html', {
        'destination': destination,
        'destination_obj': TourismRouteDestiny,
    })


def tourism_route_destination_new_admin(request):
    if request.method == 'POST':
        form = TourismRouteDestinyForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('tourism_routes-destination-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TourismRouteDestinyForm()
    return render(request, 'admin_page/tourism_routes/destinations/new.html', {
        'form': form,
    })


def tourism_route_destination_edit_admin(request, id):
    destination = TourismRouteDestiny.objects.get(id=id)
    if request.method == 'POST':
        form = TourismRouteDestinyForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(
                reverse('tourism_routes-destination-index-admin'))
    else:
        form = TourismRouteDestinyForm(instance=destination)
    return render(request, 'admin_page/tourism_routes/destinations/edit.html', {
        'destination': destination,
        'form': form,
        'destination_obj': TourismRouteDestiny
    })


def tourism_route_destination_delete_admin(request, id):
    destination = TourismRouteDestiny.objects.get(id=id)
    destination.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('tourism_routes-destination-index-admin'))


# RUTAS TURISTICAS ADMINISTRADOR

def tourism_route_index_admin(request):
    destiny = request.session['destiny_tourism_route']
    routes = TourismRoute.objects.filter(destination=destiny)
    destiny_title = TourismRouteDestiny.objects.get(id=destiny)
    destiny_id = destiny
    return render(request, 'admin_page/tourism_routes/index.html', {
        'routes': routes,
        'route_obj': TourismRoute,
        'destiny_title': destiny_title,
        'destiny_id': destiny_id,
    })


def tourism_route_show_admin(request, id):
    request.session['tourism_route'] = id
    destiny = request.session['destiny_tourism_route']
    route = TourismRoute.objects.filter(destination=destiny).get(id=id)
    destiny_title = TourismRouteDestiny.objects.get(id=destiny)
    return render(request, 'admin_page/tourism_routes/show.html', {
        'route': route,
        'route_obj': TourismRoute,
        'destiny_title': destiny_title,
    })


def tourism_route_new_admin(request):
    destiny = request.session['destiny_tourism_route']
    destiny_title = TourismRouteDestiny.objects.get(id=destiny)
    if request.method == 'POST':
        form = TourismRouteForm(request.POST, request.FILES)
        if form.is_valid():
            tourism_route = form.save(commit=False)
            tourism_route.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse(tourism_route_index_admin))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TourismRouteForm(initial={'destination': destiny})
    return render(request, 'admin_page/tourism_routes/new.html', {
        'form': form,
        'destiny_title': destiny_title,
    })


def tourism_route_edit_admin(request, id):
    destiny = request.session['destiny_tourism_route']
    route = TourismRoute.objects.filter(destination=destiny).get(id=id)
    destiny_title = TourismRouteDestiny.objects.get(id=destiny)
    if request.method == 'POST':
        form = TourismRouteForm(request.POST, request.FILES, instance=route)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('tourism_routes-show-admin', kwargs={'id': route.id}))
    else:
        form = TourismRouteForm(instance=route)
    return render(request, 'admin_page/tourism_routes/edit.html', {
        'route': route,
        'form': form,
        'tourism_route_obj': TourismRoute,
        'destiny_title': destiny_title,
    })


def tourism_route_delete_admin(request, id):
    destiny = request.session['destiny_tourism_route']
    route = TourismRoute.objects.filter(destination=destiny).get(id=id)
    route.delete()
    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(tourism_route_index_admin))


# MENU DE RUTAS TURISTICAS
def tourism_route_menu_index_admin(request):
    route = request.session['tourism_route']
    menus = TourismRouteMenu.objects.filter(route=route)
    route_title = TourismRoute.objects.get(id=route)
    route_id = route
    destiny = request.session['destiny_tourism_route']
    destiny_title = TourismRouteDestiny.objects.get(id=destiny)
    return render(request, 'admin_page/tourism_routes/menus/index.html', {
        'menus': menus,
        'menu_obj': TourismRouteMenu,
        'route_title': route_title,
        'destiny_title': destiny_title,
        'route_id': route_id,
    })


def tourism_route_menu_show_admin(request, id):
    route = request.session['tourism_route']
    menu = TourismRouteMenu.objects.filter(route=route).get(id=id)
    route_title = TourismRoute.objects.get(id=route)
    destiny = request.session['destiny_tourism_route']
    destiny_title = TourismRouteDestiny.objects.get(id=destiny)
    return render(request, 'admin_page/tourism_routes/menus/show.html', {
        'menu': menu,
        'menu_obj': TourismRouteMenu,
        'route_title': route_title,
        'destiny_title': destiny_title,
    })


def tourism_route_menu_new_admin(request):
    route = request.session['tourism_route']
    route_title = TourismRoute.objects.get(id=route)
    destiny = request.session['destiny_tourism_route']
    destiny_title = TourismRouteDestiny.objects.get(id=destiny)
    if request.method == 'POST':
        form = TourismRouteMenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('tourism_routes-menus-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TourismRouteMenuForm(initial={'route': route})
    return render(request, 'admin_page/tourism_routes/menus/new.html', {
        'form': form,
        'route_title': route_title,
        'destiny_title': destiny_title,
    })


def tourism_route_menu_edit_admin(request, id):
    route = request.session['tourism_route']
    menu = TourismRouteMenu.objects.filter(route=route).get(id=id)
    route_title = TourismRoute.objects.get(id=route)
    destiny = request.session['destiny_tourism_route']
    destiny_title = TourismRouteDestiny.objects.get(id=destiny)
    if request.method == 'POST':
        form = TourismRouteMenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('tourism_routes-menus-index-admin'))
    else:
        form = TourismRouteMenuForm(instance=menu)
    return render(request, 'admin_page/tourism_routes/menus/edit.html', {
        'menu': menu,
        'form': form,
        'menu_obj': TourismRouteMenu,
        'route_title': route_title,
        'destiny_title': destiny_title,
    })


def tourism_route_menu_delete_admin(request, id):
    route = request.session['tourism_route']
    menu = TourismRouteMenu.objects.filter(route=route).get(id=id)
    menu.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('tourism_routes-menus-index-admin'))


# HOSPEDAJES CLIENTE

def lodging_index(request):
    typeslod = LodgingType.objects.all
    return render(request, 'tour/lodging-index.html', {
        'typeslod': typeslod,
        'lodging_obj': Lodging
    })


def lodging_show(request, id):
    lod = Lodging.objects.get(id=id)
    room = LodgingRoom.objects.filter(lodging=id).order_by('price')
    schedule = LodgingSchedule.objects.filter(lodging=id).order_by('published_date')
    return render(request, 'tour/lodging-show.html', {
        'lodging': lod,
        'room': room,
        'schedule': schedule,
        'lodging_obj': Lodging
    })


# HOSPEDAJES ADMINISTRADOR

def lodging_index_admin(request):
    lodgings = Lodging.objects.all
    return render(request, 'admin_page/lodgings/index.html', {
        'lodgings': lodgings,
        'lodging_obj': Lodging
    })


def lodging_show_admin(request, id):
    lodging = Lodging.objects.get(id=id)
    room = LodgingRoom.objects.filter(lodging=id).order_by('price')
    schedule = LodgingSchedule.objects.filter(lodging=id).order_by('published_date')
    request.session['lodgings'] = id
    return render(request, 'admin_page/lodgings/show.html', {
        'lodging': lodging,
        'room': room,
        'schedule': schedule,
        'lodging_obj': Lodging
    })


def lodging_new_admin(request):
    if request.method == 'POST':
        form = LodgingForm(request.POST, request.FILES)
        if form.is_valid():
            lodging = form.save(commit=False)
            lodging.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse(lodging_index_admin))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = LodgingForm()
    return render(request, 'admin_page/lodgings/new.html', {
        'form': form,
    })


def lodging_edit_admin(request, id):
    lodging = Lodging.objects.get(id=id)

    if request.method == 'POST':
        form = LodgingForm(request.POST, request.FILES, instance=lodging)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('lodgings-show-admin', kwargs={'id': lodging.id}))
    else:
        form = LodgingForm(instance=lodging)
    return render(request, 'admin_page/lodgings/edit.html', {
        'lodgings': lodging,
        'form': form,
        'lodging_obj': Lodging
    })


def lodging_delete_admin(request, id):
    lodging = Lodging.objects.get(id=id)
    lodging.delete()
    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(lodging_index_admin))


# CUARTOS DE HOSPEDAJES
def lodging_room_index_admin(request):
    lodging = request.session['lodgings']
    rooms = LodgingRoom.objects.filter(lodging=lodging)
    lodging_title = Lodging.objects.get(id=lodging)
    lodging_id = lodging
    return render(request, 'admin_page/lodgings/rooms/index.html', {
        'rooms': rooms,
        'room_obj': LodgingRoom,
        'lodging_title': lodging_title,
        'lodging_id': lodging_id
    })


def lodging_room_show_admin(request, id):
    lodging = request.session['lodgings']
    room = LodgingRoom.objects.filter(lodging=lodging).get(id=id)
    lodging_title = Lodging.objects.get(id=lodging)
    return render(request, 'admin_page/lodgings/rooms/show.html', {
        'room': room,
        'room_obj': LodgingRoom,
        'lodging_title': lodging_title
    })


def lodging_room_new_admin(request):
    lodging = request.session['lodgings']
    lodging_title = Lodging.objects.get(id=lodging)
    if request.method == 'POST':
        form = LodgingRoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('lodgings-room-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = LodgingRoomForm(initial={'lodging': lodging})
    return render(request, 'admin_page/lodgings/rooms/new.html', {
        'form': form,
        'lodging_title': lodging_title
    })


def lodging_room_edit_admin(request, id):
    lodging = request.session['lodgings']
    room = LodgingRoom.objects.filter(lodging=lodging).get(id=id)
    lodging_title = Lodging.objects.get(id=lodging)
    if request.method == 'POST':
        form = LodgingRoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('lodgings-room-index-admin'))
    else:
        form = LodgingRoomForm(instance=room)
    return render(request, 'admin_page/lodgings/rooms/edit.html', {
        'room': room,
        'form': form,
        'room_obj': LodgingRoom,
        'lodging_title': lodging_title
    })


def lodging_room_delete_admin(request, id):
    lodging = request.session['lodgings']
    room = LodgingRoom.objects.filter(lodging=lodging).get(id=id)
    room.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('lodgings-room-index-admin'))


# HORARIOS DE HOSPEDAJES

def lodging_schedule_index_admin(request):
    lodging = request.session['lodgings']
    schedules = LodgingSchedule.objects.filter(lodging=lodging)
    lodging_title = Lodging.objects.get(id=lodging)
    lodging_id = lodging
    return render(request, 'admin_page/lodgings/schedules/index.html', {
        'schedules': schedules,
        'schedule_obj': LodgingSchedule,
        'lodging_title': lodging_title,
        'lodging_id': lodging_id
    })


def lodging_schedule_show_admin(request, id):
    lodging = request.session['lodgings']
    schedule = LodgingSchedule.objects.filter(lodging=lodging).get(id=id)
    lodging_title = Lodging.objects.get(id=lodging)
    return render(request, 'admin_page/lodgings/schedules/show.html', {
        'schedule': schedule,
        'schedule_obj': LodgingSchedule,
        'lodging_title': lodging_title
    })


def lodging_schedule_new_admin(request):
    lodging = request.session['lodgings']
    lodging_title = Lodging.objects.get(id=lodging)
    if request.method == 'POST':
        form = LodgingScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('lodgings-schedules-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = LodgingScheduleForm(initial={'lodging': lodging})
    return render(request, 'admin_page/lodgings/schedules/new.html', {
        'form': form,
        'lodging_title': lodging_title
    })


def lodging_schedule_edit_admin(request, id):
    lodging = request.session['lodgings']
    schedule = LodgingSchedule.objects.filter(lodging=lodging).get(id=id)
    lodging_title = Lodging.objects.get(id=lodging)
    if request.method == 'POST':
        form = LodgingScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('lodgings-schedules-show-admin', kwargs={'id': schedule.id}))
    else:
        form = LodgingScheduleForm(instance=schedule)
    return render(request, 'admin_page/lodgings/schedules/edit.html', {
        'schedule': schedule,
        'form': form,
        'schedule_obj': LodgingSchedule,
        'lodging_title': lodging_title
    })


def lodging_schedule_delete_admin(request, id):
    lodging = request.session['lodgings']
    schedule = LodgingSchedule.objects.filter(lodging=lodging).get(id=id)
    schedule.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('lodgings-schedules-index-admin'))


# TIPOS DE HOSPEDAJES

def lodging_type_index_admin(request):
    types = LodgingType.objects.all
    return render(request, 'admin_page/lodgings/types/index.html', {
        'types': types,
        'type_obj': LodgingType,
    })


def lodging_type_show_admin(request, id):
    type = LodgingType.objects.get(id=id)
    return render(request, 'admin_page/lodgings/types/show.html', {
        'type': type,
        'type_obj': LodgingType,
    })


def lodging_type_new_admin(request):
    if request.method == 'POST':
        form = LodgingTypeForm(request.POST, request.FILES)
        if form.is_valid():
            type = form.save(commit=False)
            type.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('lodgings-types-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = LodgingTypeForm()
    return render(request, 'admin_page/lodgings/types/new.html', {
        'form': form,
    })


def lodging_type_edit_admin(request, id):
    type = LodgingType.objects.get(id=id)
    if request.method == 'POST':
        form = LodgingTypeForm(request.POST, request.FILES, instance=type)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('lodgings-types-index-admin'))
    else:
        form = LodgingTypeForm(instance=type)
    return render(request, 'admin_page/lodgings/types/edit.html', {
        'type': type,
        'form': form,
        'type_obj': LodgingType
    })


def lodging_type_delete_admin(request, id):
    type = LodgingType.objects.get(id=id)
    type.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('lodgings-types-index-admin'))


# SERVICIOS DE HOSPEDAJES

def lodging_service_index_admin(request):
    services = LodgingService.objects.all
    return render(request, 'admin_page/lodgings/services/index.html', {
        'services': services,
        'service_obj': LodgingService,
    })


def lodging_service_show_admin(request, id):
    service = LodgingService.objects.get(id=id)
    return render(request, 'admin_page/lodgings/services/show.html', {
        'service': service,
        'service_obj': LodgingService,
    })


def lodging_service_new_admin(request):
    if request.method == 'POST':
        form = LodgingServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('lodgings-services-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = LodgingServiceForm()
    return render(request, 'admin_page/lodgings/services/new.html', {
        'form': form,
    })


def lodging_service_edit_admin(request, id):
    service = LodgingService.objects.get(id=id)
    if request.method == 'POST':
        form = LodgingServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('lodgings-services-index-admin'))
    else:
        form = LodgingServiceForm(instance=service)
    return render(request, 'admin_page/lodgings/services/edit.html', {
        'service': service,
        'form': form,
        'service_obj': LodgingService
    })


def lodging_service_delete_admin(request, id):
    service = LodgingService.objects.get(id=id)
    service.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('lodgings-services-index-admin'))
