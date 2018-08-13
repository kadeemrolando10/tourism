from functools import reduce

from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q

from tour.models import Event, Restaurant, TourismSite, Transport, Lodging, Agency, Objective, Function, \
    TransportDestination, LodgingRoom, LodgingType, Location, LodgingSchedule, TourismRoute, TourismSiteSchedule, \
    TransportSchedule, RestaurantSchedule, LodgingService, AgencyService, \
    AgencySchedule, RestaurantService, RestaurantMenu, TransportService, TransportTypeService, TourismSiteMenu, \
    TourismSiteType, TourismSiteService, TourismRouteMenu, Law, Client, ROLE_USERS, Secretary

from tour.forms import RestaurantForm, AgencyForm, EventForm, TransportForm, TourismSiteForm, TourismRouteForm, \
    LodgingForm, AgencyServiceForm, AgencyScheduleForm, RestaurantMenuForm, RestaurantScheduleForm, \
    RestaurantServiceForm, TransportDestinationForm, TransportServiceForm, TransportTypeServiceForm, \
    TransportScheduleForm, TourismSiteMenuForm, TourismSiteScheduleForm, LocationForm, TourismSiteTypeForm, \
    TourismSiteServiceForm, TourismRouteMenuForm, LodgingRoomForm, LodgingScheduleForm, \
    LodgingTypeForm, LodgingServiceForm, ClientForm, ClientFormEdit, ObjectiveForm, FunctionForm, LawForm, SecretaryForm


def user_index(request):
    users_list = Client.objects.all()
    query = request.GET.get('q')
    if query:
        users_list = users_list.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).distinct()
    paginator = Paginator(users_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    users = paginator.get_page(page)

    template = 'registration/user/index.html'
    params = {'users': users, 'role_users': ROLE_USERS}

    if request.is_ajax():
        template = 'registration/user/users.html'
        params = {'users': users}

    return render(request, template, params)


def user_new(request):
    if request.method == 'POST':
        formUser = UserCreationForm(request.POST)
        form = ClientForm(request.POST)
        if formUser.is_valid() and form.is_valid():
            user = formUser.save()
            client = form.save(commit=False)
            client.user = user
            client.save()

            if client.rol == 'AD':  # ADMINISTRADOR
                g = Group.objects.get(id=1)
                g.user_set.add(user.id)
            elif client.rol == 'US':  # USUARIO
                g = Group.objects.get(id=2)
                g.user_set.add(user.id)

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse(user_index))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        formUser = UserCreationForm()
        form = ClientForm()
    return render(request, 'registration/user/new.html', {
        'form': form,
        'form_second': formUser,
    })


def user_edit(request, id):
    client = Client.objects.get(id=id)

    if request.method == 'POST':
        form = ClientFormEdit(request.POST, instance=client)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('user-index'))
    else:
        form = ClientFormEdit(instance=client)
    return render(request, 'registration/user/edit.html', {
        'form': form,
        'client': client
    })


def user_delete(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    is_exist = Client.objects.filter(id=id).exists()

    if is_exist:
        message = 'No se pudo eliminar'
        messages.add_message(request, messages.ERROR, message)
    else:
        message = 'Eliminado!'
        messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(user_index))


def index_admin(request):
    return render(request, 'admin_page/index.html', {})


def change_main(request, id):
    request.session['id_main'] = id
    return HttpResponseRedirect(reverse(index))


def index(request):
    events = Event.objects.all
    restaurants = Restaurant.objects.all
    transports = Transport.objects.all
    tourism_sites = Restaurant.objects.all
    agencies = Agency.objects.all
    lodgings = Lodging.objects.all
    return render(request, 'tour/index.html', {
        'events': events,
        'restaurants': restaurants,
        'transports': transports,
        'tourism_sites': tourism_sites,
        'agencys': agencies,
        'lodgings': lodgings
    })


def secretary(request):
    objectives = Objective.objects.all
    secretaries = Secretary.objects.all
    laws = Law.objects.all
    functions = Function.objects.all
    return render(request, 'tour/secretary.html', {
        'objectives': objectives,
        'secretaries': secretaries,
        'laws': laws,
        'functions': functions
    })


# AGENCIAS DE TURISMO CLIENTE


def agency_index(request):
    ids = request.session['id_main']
    if ids is None:
        agencies = Agency.objects.all
    else:
        agencies = Agency.objects.filter(destination=ids)
    return render(request, 'tour/agencies-index.html', {
        'agencies': agencies,
        'agency_obj': Agency,
    })


def agency_show(request, id):
    agency = Agency.objects.get(id=id)
    services = AgencyService.objects.filter(agency=id)
    schedule = AgencySchedule.objects.filter(agency=id)
    score = round(agency.score / 2);
    return render(request, 'tour/agencies-show.html', {
        'agency': agency,
        'agency_obj': Agency,
        'services': services,
        'schedule': schedule,
        'score': score
    })


# AGENCIAS DE TURISMO ADMINISTRADOR


def agency_index_admin(request):
    agencies_list = Agency.objects.all()
    query = request.GET.get('q')
    if query:
        agencies_list = agencies_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(agencies_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    agencies = paginator.get_page(page)

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
    services_list = AgencyService.objects.filter(agency=agency)
    query = request.GET.get('q')
    if query:
        services_list = services_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(services_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    services = paginator.get_page(page)
    agency_title = Agency.objects.get(id=agency)
    return render(request, 'admin_page/agencies/services/index.html', {
        'services': services,
        'service_obj': AgencyService,
        'agency_title': agency_title,
        'agency_id': agency
    })


def agency_service_show_admin(request, id):
    agency = request.session['agency']
    service = AgencyService.objects.filter(agency=agency).get(id=id)
    agency_title = Agency.objects.get(id=agency)
    return render(request, 'admin_page/agencies/services/show.html', {
        'service': service,
        'service_obj': AgencyService,
        'agency_title': agency_title,
        'agency_id': agency
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
        'agency_title': agency_title,
        'agency_id': agency
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
        'agency_title': agency_title,
        'agency_id': agency
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
    schedules_list = AgencySchedule.objects.filter(agency=agency)
    query = request.GET.get('q')
    if query:
        schedules_list = schedules_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(schedules_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    schedules = paginator.get_page(page)
    agency_title = Agency.objects.get(id=agency)
    return render(request, 'admin_page/agencies/schedules/index.html', {
        'schedules': schedules,
        'schedule_obj': AgencySchedule,
        'agency_title': agency_title,
        'agency_id': agency
    })


def agency_schedule_show_admin(request, id):
    agency = request.session['agency']
    schedule = AgencySchedule.objects.filter(agency=agency).get(id=id)
    agency_title = Agency.objects.get(id=agency)
    return render(request, 'admin_page/agencies/schedules/show.html', {
        'schedule': schedule,
        'schedule_obj': AgencySchedule,
        'agency_title': agency_title,
        'agency_id': agency
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
        'agency_title': agency_title,
        'agency_id': agency
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
        'agency_title': agency_title,
        'agency_id': agency
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
    id = request.session['id_main']
    if id is None:
        events = Event.objects.all
    else:
        events = Event.objects.filter(destination=id)
    return render(request, 'tour/events-index.html', {
        'events': events,
        'event_obj': Event
    })


# EVENTOS ADMINISTRADOR

def event_index_admin(request):
    events_list = Event.objects.all()
    query = request.GET.get('q')
    if query:
        events_list = events_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(events_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    events = paginator.get_page(page)
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
    id = request.session['id_main']
    if id is None:
        restaurants = Restaurant.objects.all
    else:
        restaurants = Restaurant.objects.filter(destination=id)

    return render(request, 'tour/restaurants-index.html', {
        'restaurants': restaurants,
        'restaurant_obj': Restaurant
    })


def restaurant_show(request, id):
    restaurant = Restaurant.objects.get(id=id)
    menu = RestaurantMenu.objects.filter(restaurant=id).order_by('price')
    schedule = RestaurantSchedule.objects.filter(restaurant=id).order_by('register_at')
    score = round(restaurant.score / 2);

    soups = RestaurantMenu.objects.filter(restaurant=id, category='SO').order_by('price')
    entrances = RestaurantMenu.objects.filter(restaurant=id, category='EN').order_by('price')
    seconds = RestaurantMenu.objects.filter(restaurant=id, category='SE').order_by('price')
    sweets = RestaurantMenu.objects.filter(restaurant=id, category='PO').order_by('price')
    wines = RestaurantMenu.objects.filter(restaurant=id, category='CV').order_by('price')
    breakfast = RestaurantMenu.objects.filter(restaurant=id, category='DE').order_by('price')
    drinks = RestaurantMenu.objects.filter(restaurant=id, category='BE').order_by('price')

    return render(request, 'tour/restaurants-show.html', {
        'restaurant': restaurant,
        'restaurant_obj': Restaurant,
        'schedule': schedule,
        'menu': menu,
        'score': score,
        'soups': soups,
        'entrances': entrances,
        'seconds': seconds,
        'sweets': sweets,
        'wines': wines,
        'breakfast': breakfast,
        'drinks': drinks
    })

    # RESTAURANTS ADMINISTRADOR


def restaurant_index_admin(request):
    restaurants_list = Restaurant.objects.all()
    query = request.GET.get('q')
    if query:
        restaurants_list = restaurants_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(restaurants_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    restaurants = paginator.get_page(page)
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
            restaurant = form.save(commit=True)
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
    menus_list = RestaurantMenu.objects.filter(restaurant=restaurant)
    query = request.GET.get('q')
    if query:
        menus_list = menus_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(menus_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    menus = paginator.get_page(page)
    restaurant_title = Restaurant.objects.get(id=restaurant)
    return render(request, 'admin_page/restaurants/menus/index.html', {
        'menus': menus,
        'menu_obj': RestaurantMenu,
        'restaurant_title': restaurant_title,
        'restaurant_id': restaurant
    })


def restaurant_menu_show_admin(request, id):
    restaurant = request.session['restaurants']
    menu = RestaurantMenu.objects.filter(restaurant=restaurant).get(id=id)
    restaurant_title = Restaurant.objects.get(id=restaurant)
    return render(request, 'admin_page/restaurants/menus/show.html', {
        'menu': menu,
        'menu_obj': RestaurantMenu,
        'restaurant_title': restaurant_title,
        'restaurant_id': restaurant
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
        'restaurant_title': restaurant_title,
        'restaurant_id': restaurant
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
        'restaurant_title': restaurant_title,
        'restaurant_id': restaurant
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
    schedules_list = RestaurantSchedule.objects.filter(restaurant=restaurant)
    query = request.GET.get('q')
    if query:
        schedules_list = schedules_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(schedules_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    schedules = paginator.get_page(page)
    restaurant_title = Restaurant.objects.get(id=restaurant)
    return render(request, 'admin_page/restaurants/schedules/index.html', {
        'schedules': schedules,
        'schedule_obj': RestaurantSchedule,
        'restaurant_title': restaurant_title,
        'restaurant_id': restaurant
    })


def restaurant_schedule_show_admin(request, id):
    restaurant = request.session['restaurants']
    schedule = RestaurantSchedule.objects.filter(restaurant=restaurant).get(id=id)
    restaurant_title = Restaurant.objects.get(id=restaurant)
    return render(request, 'admin_page/restaurants/schedules/show.html', {
        'schedule': schedule,
        'schedule_obj': RestaurantSchedule,
        'restaurant_title': restaurant_title,
        'restaurant_id': restaurant
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
        'restaurant_title': restaurant_title,
        'restaurant_id': restaurant
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
        'restaurant_title': restaurant_title,
        'restaurant_id': restaurant
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
    services_list = RestaurantService.objects.all
    query = request.GET.get('q')
    if query:
        services_list = services_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(services_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    services = paginator.get_page(page)
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
    id = request.session['id_main']
    if id is None:
        transports = Transport.objects.all
    else:
        transports = Transport.objects.filter(destination=id)

    return render(request, 'tour/transports-index.html', {
        'transports': transports,
        'transport_obj': Transport
    })


def transport_show(request, id):
    transport = Transport.objects.get(id=id)
    schedule = TransportSchedule.objects.filter(transport=id).order_by('register_at')
    destinations = TransportDestination.objects.filter(transport__id=id)
    score = round(transport.score / 2);
    return render(request, 'tour/transports-show.html', {
        'transport': transport,
        'destinations': destinations,
        'schedule': schedule,
        'score': score,
        'transport_obj': Transport
    })


# TRANSPORTES ADMINISTRADOR

def transport_index_admin(request):
    transports_list = Transport.objects.all()
    query = request.GET.get('q')
    if query:
        transports_list = transports_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(transports_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    transports = paginator.get_page(page)
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
    destinations_list = TransportDestination.objects.filter(transport=transport)
    query = request.GET.get('q')
    if query:
        destinations_list = destinations_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(destinations_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    destinations = paginator.get_page(page)

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
    request.session['destination'] = id
    return HttpResponseRedirect(reverse(transport_type_service_index_admin))


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
        'transport_title': transport_title,
        'transport_id': transport
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
        'transport_title': transport_title,
        'transport_id': transport
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
    services_list = TransportService.objects.all()
    query = request.GET.get('q')
    if query:
        services_list = services_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(services_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    services = paginator.get_page(page)
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
    transport_title = Transport.objects.get(id=transport)
    destination_id = request.session['destination']
    destination_title = TransportDestination.objects.get(id=destination_id)
    destination = TransportDestination.objects.filter(transport=transport).get(id=destination_id)
    type_services_list = TransportTypeService.objects.filter(destination=destination_id)
    query = request.GET.get('q')
    if query:
        type_services_list = type_services_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(type_services_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    type_services = paginator.get_page(page)

    return render(request, 'admin_page/transports/type_services/index.html', {
        'type_services': type_services,
        'type_service_obj': TransportTypeService,
        'transport_title': transport_title,
        'destination_title': destination_title,
        'destination_id': destination_id,
        'destination': destination,
        'destination_obj': TransportDestination,
        'transport_id': transport

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
        'destination_title': destination_title,
        'transport_id': transport
    })


def transport_type_service_new_admin(request):
    transport = request.session['transports']
    destination = request.session['destination']
    transport_title = Transport.objects.get(id=transport)
    destination_title = TransportDestination.objects.get(id=destination)
    if request.method == 'POST':
        form = TransportTypeServiceForm(request.POST, request.FILES)
        if form.is_valid():
            type_service = form.save(commit=True)
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
        'destination_title': destination_title,
        'transport_id': transport
    })


def transport_type_service_edit_admin(request, id):
    transport = request.session['transports']
    destination = request.session['destination']
    type_service = TransportTypeService.objects.filter(destination=destination).get(id=id)
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
        'destination_title': destination_title,
        'transport_id': transport
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
    schedules_list = TransportSchedule.objects.filter(transport=transport)
    query = request.GET.get('q')
    if query:
        schedules_list = schedules_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(schedules_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    schedules = paginator.get_page(page)

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
    id = request.session['id_main']
    if id is None:
        sites = TourismSite.objects.all
    else:
        sites = TourismSite.objects.filter(destination=id)
    return render(request, 'tour/tourism_sites-index.html', {
        'sites': sites,
        'tourism_site_obj': TourismSite
    })


def tourism_site_show(request, id):
    site = TourismSite.objects.get(id=id)
    schedule = TourismSiteSchedule.objects.filter(site=id).order_by('register_at')
    score = round(site.score / 2)
    return render(request, 'tour/tourism_site-show.html', {
        'site': site,
        'schedule': schedule,
        'score': score
    })


# SITIOS TURISTICOS ADMINISTRADOR

def tourism_site_index_admin(request):
    sites_list = TourismSite.objects.all()
    query = request.GET.get('q')
    if query:
        sites_list = sites_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(sites_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    sites = paginator.get_page(page)
    return render(request, 'admin_page/tourism_sites/index.html', {
        'sites': sites,
        'site_obj': TourismSite
    })


def tourism_site_show_admin(request, id):
    site = TourismSite.objects.get(id=id)
    request.session['tourism_site'] = id
    return render(request, 'admin_page/tourism_sites/show.html', {
        'site': site,
        'site_obj': TourismSite,
    })


def tourism_site_new_admin(request):
    if request.method == 'POST':
        form = TourismSiteForm(request.POST, request.FILES)
        if form.is_valid():
            tourism_site = form.save(commit=True)
            tourism_site.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse(tourism_site_index_admin))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = TourismSiteForm()
    return render(request, 'admin_page/tourism_sites/new.html', {
        'form': form
    })


def tourism_site_edit_admin(request, id):
    tourism_site = TourismSite.objects.get(id=id)

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
        'tourism_site_obj': TourismSite
    })


def tourism_site_delete_admin(request, id):
    tourism_site = TourismSite.objects.get(id=id)
    tourism_site.delete()
    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(tourism_site_index_admin))


# MENU DE SITIOS TURISTICOS

def tourism_site_menu_index_admin(request):
    tourism_site = request.session['tourism_site']
    menus_list = TourismSiteMenu.objects.filter(site=tourism_site)
    query = request.GET.get('q')
    if query:
        menus_list = menus_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(menus_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    menus = paginator.get_page(page)

    site_title = TourismSite.objects.get(id=tourism_site)
    return render(request, 'admin_page/tourism_sites/menus/index.html', {
        'menus': menus,
        'menu_obj': TourismSiteMenu,
        'site_title': site_title,
        'site_id': tourism_site
    })


def tourism_site_menu_show_admin(request, id):
    tourism_site = request.session['tourism_site']
    menu = TourismSiteMenu.objects.filter(site=tourism_site).get(id=id)
    tourism_site_title = TourismSite.objects.get(id=tourism_site)
    return render(request, 'admin_page/tourism_sites/menus/show.html', {
        'menu': menu,
        'menu_obj': TourismSiteMenu,
        'tourism_site_title': tourism_site_title,
        'site_id': tourism_site
    })


def tourism_site_menu_new_admin(request):
    tourism_site = request.session['tourism_site']
    site_title = TourismSite.objects.get(id=tourism_site)
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
        'site_id': tourism_site
    })


def tourism_site_menu_edit_admin(request, id):
    tourism_site = request.session['tourism_site']
    menu = TourismSiteMenu.objects.filter(site=tourism_site).get(id=id)
    site_title = TourismSite.objects.get(id=tourism_site)
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
        'site_id': tourism_site
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
    schedules_list = TourismSiteSchedule.objects.filter(site=tourism_site)
    query = request.GET.get('q')
    if query:
        schedules_list = schedules_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(schedules_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    schedules = paginator.get_page(page)
    site_title = TourismSite.objects.get(id=tourism_site)
    return render(request, 'admin_page/tourism_sites/schedules/index.html', {
        'schedules': schedules,
        'schedule_obj': TourismSiteSchedule,
        'site_title': site_title,
        'site_id': tourism_site
    })


def tourism_site_schedule_show_admin(request, id):
    tourism_site = request.session['tourism_site']
    schedule = TourismSiteSchedule.objects.filter(tourism_site=tourism_site).get(id=id)
    tourism_site_title = TourismSite.objects.get(id=tourism_site)
    return render(request, 'admin_page/tourism_sites/schedules/show.html', {
        'schedule': schedule,
        'schedule_obj': TourismSiteSchedule,
        'tourism_site_title': tourism_site_title,
        'site_id': tourism_site
    })


def tourism_site_schedule_new_admin(request):
    tourism_site = request.session['tourism_site']
    site_title = TourismSite.objects.get(id=tourism_site)
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
        'site_id': tourism_site
    })


def tourism_site_schedule_edit_admin(request, id):
    tourism_site = request.session['tourism_site']
    schedule = TourismSiteSchedule.objects.filter(site=tourism_site).get(id=id)
    site_title = TourismSite.objects.get(id=tourism_site)
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
        'site_id': tourism_site
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
    types_list = TourismSiteType.objects.all()
    query = request.GET.get('q')
    if query:
        types_list = types_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(types_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    types = paginator.get_page(page)
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
    services_list = TourismSiteService.objects.all()
    query = request.GET.get('q')
    if query:
        services_list = services_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(services_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    services = paginator.get_page(page)
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
    id = request.session['id_main']
    if id is None:
        routes = TourismRoute.objects.all
    else:
        routes = TourismRoute.objects.filter(destination=id)
    return render(request, 'tour/tourism_route-index.html', {
        'routes': routes,
        'tourism_route_obj': TourismRoute
    })


def tourism_route_show(request, id):
    route = TourismRoute.objects.get(id=id)
    score = round(route.score / 2)
    return render(request, 'tour/tourism_route-show.html', {
        'route': route,
        'score': score
    })


# RUTAS TURISTICAS ADMINISTRADOR

def tourism_route_index_admin(request):
    routes_list = TourismRoute.objects.all()
    query = request.GET.get('q')
    if query:
        routes_list = routes_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(routes_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    routes = paginator.get_page(page)
    return render(request, 'admin_page/tourism_routes/index.html', {
        'routes': routes,
        'route_obj': TourismRoute
    })


def tourism_route_show_admin(request, id):
    request.session['tourism_route'] = id
    route = TourismRoute.objects.get(id=id)
    return render(request, 'admin_page/tourism_routes/show.html', {
        'route': route,
        'route_obj': TourismRoute
    })


def tourism_route_new_admin(request):
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
        form = TourismRouteForm()
    return render(request, 'admin_page/tourism_routes/new.html', {
        'form': form,
    })


def tourism_route_edit_admin(request, id):
    route = TourismRoute.objects.get(id=id)
    if request.method == 'POST':
        form = TourismRouteForm(request.POST, request.FILES, instance=route)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('tourism_routes-index-admin'))
    else:
        form = TourismRouteForm(instance=route)
    return render(request, 'admin_page/tourism_routes/edit.html', {
        'route': route,
        'form': form,
        'tourism_route_obj': TourismRoute
    })


def tourism_route_delete_admin(request, id):
    route = TourismRoute.objects.get(id=id)
    route.delete()
    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(tourism_route_index_admin))


# MENU DE RUTAS TURISTICAS
def tourism_route_menu_index_admin(request):
    route = request.session['tourism_route']
    menus_list = TourismRouteMenu.objects.filter(route=route)
    query = request.GET.get('q')
    if query:
        menus_list = menus_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(menus_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    menus = paginator.get_page(page)

    route_title = TourismRoute.objects.get(id=route)
    return render(request, 'admin_page/tourism_routes/menus/index.html', {
        'menus': menus,
        'menu_obj': TourismRouteMenu,
        'route_title': route_title,
        'route_id': route,
    })


def tourism_route_menu_show_admin(request, id):
    route = request.session['tourism_route']
    menu = TourismRouteMenu.objects.filter(route=route).get(id=id)
    route_title = TourismRoute.objects.get(id=route)
    return render(request, 'admin_page/tourism_routes/menus/show.html', {
        'menu': menu,
        'menu_obj': TourismRouteMenu,
        'route_title': route_title,
        'route_id': route,
    })


def tourism_route_menu_new_admin(request):
    route = request.session['tourism_route']
    route_title = TourismRoute.objects.get(id=route)
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
        'route_id': route,
    })


def tourism_route_menu_edit_admin(request, id):
    route = request.session['tourism_route']
    menu = TourismRouteMenu.objects.filter(route=route).get(id=id)
    route_title = TourismRoute.objects.get(id=route)
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
        'route_id': route,
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
    id = request.session['id_main']
    if id is None:
        lodgings = Lodging.objects.all
    else:
        lodgings = Lodging.objects.filter(destination=id)
    return render(request, 'tour/lodging-index.html', {
        'lodgings': lodgings,
        'lodging_obj': Lodging
    })


def lodging_show(request, id):
    lodging = Lodging.objects.get(id=id)
    room = LodgingRoom.objects.filter(lodging=id).order_by('price')
    schedule = LodgingSchedule.objects.filter(lodging=id).order_by('register_at')
    score = round(lodging.score / 2);
    return render(request, 'tour/lodging-show.html', {
        'lodging': lodging,
        'room': room,
        'schedule': schedule,
        'lodging_obj': Lodging,
        'score': score
    })


# HOSPEDAJES ADMINISTRADOR

def lodging_index_admin(request):
    lodgings_list = Lodging.objects.all()
    query = request.GET.get('q')
    if query:
        lodgings_list = lodgings_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(lodgings_list, 10)  # Show 10  per page
    page = request.GET.get('page')
    lodgings = paginator.get_page(page)
    return render(request, 'admin_page/lodgings/index.html', {
        'lodgings': lodgings,
        'lodging_obj': Lodging
    })


def lodging_show_admin(request, id):
    lodging = Lodging.objects.get(id=id)
    room = LodgingRoom.objects.filter(lodging=id).order_by('price')
    schedule = LodgingSchedule.objects.filter(lodging=id).order_by('register_at')
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
            lodging = form.save(commit=True)
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
    rooms_list = LodgingRoom.objects.filter(lodging=lodging)
    query = request.GET.get('q')
    if query:
        rooms_list = rooms_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(rooms_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    rooms = paginator.get_page(page)
    lodging_title = Lodging.objects.get(id=lodging)
    return render(request, 'admin_page/lodgings/rooms/index.html', {
        'rooms': rooms,
        'room_obj': LodgingRoom,
        'lodging_title': lodging_title,
        'lodging_id': lodging
    })


def lodging_room_show_admin(request, id):
    lodging = request.session['lodgings']
    room = LodgingRoom.objects.filter(lodging=lodging).get(id=id)
    lodging_title = Lodging.objects.get(id=lodging)
    return render(request, 'admin_page/lodgings/rooms/show.html', {
        'room': room,
        'room_obj': LodgingRoom,
        'lodging_title': lodging_title,
        'lodging_id': lodging
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
        'lodging_title': lodging_title,
        'lodging_id': lodging
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
        'lodging_title': lodging_title,
        'lodging_id': lodging
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
    schedules_list = LodgingSchedule.objects.filter(lodging=lodging)
    query = request.GET.get('q')
    if query:
        schedules_list = schedules_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(schedules_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    schedules = paginator.get_page(page)
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
        'lodging_title': lodging_title,
        'lodging_id': lodging
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
        'lodging_title': lodging_title,
        'lodging_id': lodging
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
    types_list = LodgingType.objects.all()
    query = request.GET.get('q')
    if query:
        types_list = types_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(types_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    types = paginator.get_page(page)
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
    services_list = LodgingService.objects.all()
    query = request.GET.get('q')
    if query:
        services_list = services_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(services_list, 10)  # Show 10  per page
    page = request.GET.get('page')
    services = paginator.get_page(page)
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


# LOCALIZACIONES

def location_index_admin(request):
    destinations_list = Location.objects.all()
    query = request.GET.get('q')
    if query:
        destinations_list = destinations_list.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(destinations_list, 10)  # Show 15 contacts per page
    page = request.GET.get('page')
    destinations = paginator.get_page(page)
    return render(request, 'admin_page/locations/index.html', {
        'destinations': destinations,
        'destination_obj': Location,
    })


def location_show_admin(request, id):
    destination = Location.objects.get(id=id)
    return render(request, 'admin_page/locations/show.html', {
        'destination': destination,
        'destination_obj': Location,
    })


def location_new_admin(request):
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('location-index-admin'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = LocationForm()
    return render(request, 'admin_page/locations/new.html', {
        'form': form,
    })


def location_edit_admin(request, id):
    destination = Location.objects.get(id=id)
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('location-index-admin'))
    else:
        form = LocationForm(instance=destination)
    return render(request, 'admin_page/locations/edit.html', {
        'destination': destination,
        'form': form,
        'destination_obj': Location
    })


def location_delete_admin(request, id):
    destination = Location.objects.get(id=id)
    destination.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('location-index-admin'))


# CONFIGURACIONES

def configuration_index(request):
    objectives = Objective.objects.all
    secretaries = Secretary.objects.all
    laws = Law.objects.all
    functions = Function.objects.all
    return render(request, 'admin_page/configurations/index.html', {
        'objectives': objectives,
        'secretaries': secretaries,
        'laws': laws,
        'functions': functions
    })


# OBJETIVOS

def objective_new(request):
    if request.method == 'POST':
        form = ObjectiveForm(request.POST, request.FILES)
        if form.is_valid():
            objective = form.save(commit=False)
            objective.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('configurations-index'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = ObjectiveForm()
    return render(request, 'admin_page/configurations/objectives/new.html', {
        'form': form,
    })


def objective_edit(request, id):
    objective = Objective.objects.get(id=id)
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES, instance=objective)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('configurations-index'))
    else:
        form = LocationForm(instance=objective)
    return render(request, 'admin_page/configurations/objectives/edit.html', {
        'objective': objective,
        'form': form,
        'objective_obj': Objective
    })


def objective_delete(request, id):
    objective = Objective.objects.get(id=id)
    objective.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('configurations-index'))


# FUNCIONES

def function_new(request):
    if request.method == 'POST':
        form = FunctionForm(request.POST, request.FILES)
        if form.is_valid():
            function = form.save(commit=False)
            function.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('configurations-index'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = FunctionForm()
    return render(request, 'admin_page/configurations/functions/new.html', {
        'form': form,
    })


def function_edit(request, id):
    function = Function.objects.get(id=id)
    if request.method == 'POST':
        form = FunctionForm(request.POST, request.FILES, instance=function)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('configurations-index'))
    else:
        form = FunctionForm(instance=function)
    return render(request, 'admin_page/configurations/functions/edit.html', {
        'function': function,
        'form': form,
        'function_obj': Function
    })


def function_delete(request, id):
    function = Function.objects.get(id=id)
    function.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('configurations-index'))


# LEYES

def law_new(request):
    if request.method == 'POST':
        form = LawForm(request.POST, request.FILES)
        if form.is_valid():
            law = form.save(commit=False)
            law.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('configurations-index'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = LawForm()
    return render(request, 'admin_page/configurations/laws/new.html', {
        'form': form,
    })


def law_edit(request, id):
    law = Law.objects.get(id=id)
    if request.method == 'POST':
        form = LawForm(request.POST, request.FILES, instance=law)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('configurations-index'))
    else:
        form = LawForm(instance=law)
    return render(request, 'admin_page/configurations/laws/edit.html', {
        'law': law,
        'form': form,
        'law_obj': Law
    })


def law_delete(request, id):
    law = Law.objects.get(id=id)
    law.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('configurations-index'))


# SECRETARIO

def secretary_new(request):
    if request.method == 'POST':
        form = SecretaryForm(request.POST, request.FILES)
        if form.is_valid():
            secretary = form.save(commit=False)
            secretary.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('configurations-index'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = SecretaryForm()
    return render(request, 'admin_page/configurations/secretary/new.html', {
        'form': form,
    })


def secretary_edit(request, id):
    secretary = Secretary.objects.get(id=id)
    if request.method == 'POST':
        form = SecretaryForm(request.POST, request.FILES, instance=secretary)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('configurations-index'))
    else:
        form = SecretaryForm(instance=secretary)
    return render(request, 'admin_page/configurations/secretary/edit.html', {
        'secretary': secretary,
        'form': form,
        'secretary_obj': Secretary
    })


def secretary_delete(request, id):
    secretary = Secretary.objects.get(id=id)
    secretary.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('configurations-index'))
