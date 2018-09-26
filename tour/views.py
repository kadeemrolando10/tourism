from django.contrib.auth.decorators import permission_required, login_required
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
    TourismSiteType, TourismSiteService, TourismRouteMenu, Law, Client, ROLE_USERS, Secretary, Social, AssignmentSite, \
    AssignmentTransport, AssignmentRestaurant, AssignmentAgency, AssignmentLodging

from tour.forms import RestaurantForm, AgencyForm, EventForm, TransportForm, TourismSiteForm, TourismRouteForm, \
    LodgingForm, AgencyServiceForm, AgencyScheduleForm, RestaurantMenuForm, RestaurantScheduleForm, \
    RestaurantServiceForm, TransportDestinationForm, TransportServiceForm, TransportTypeServiceForm, \
    TransportScheduleForm, TourismSiteMenuForm, TourismSiteScheduleForm, LocationForm, TourismSiteTypeForm, \
    TourismSiteServiceForm, TourismRouteMenuForm, LodgingRoomForm, LodgingScheduleForm, \
    LodgingTypeForm, LodgingServiceForm, ClientForm, ClientFormEdit, ObjectiveForm, FunctionForm, LawForm, \
    SecretaryForm, SocialForm, AssignmentSiteForm, AssignmentTransportForm, AssignmentRestaurantForm, \
    AssignmentAgencyForm, AssignmentLodgingForm


# PAGINA NOTICACIONES ADMINISTRADOR
@login_required
def notification(request):
    restaurants = Restaurant.objects.filter(is_active=False)
    transports = Transport.objects.filter(is_active=False)
    tourism_sites = TourismSite.objects.filter(is_active=False)
    agencies = Agency.objects.filter(is_active=False)
    lodgings = Lodging.objects.filter(is_active=False)
    return render(request, 'admin_page/notifications.html', {
        'restaurants': restaurants,
        'transports': transports,
        'sites': tourism_sites,
        'agencies': agencies,
        'lodgings': lodgings,
    })


# USUARIOS ADMINISTRADOR

@permission_required('tour.index_client', login_url='/accounts/login/')
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


@permission_required('tour.add_client', login_url='/accounts/login/')
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
                client.user.is_superuser = True
                client.save()
            elif client.rol == 'US-L':  # USUARIO HOSPEDAJE
                g = Group.objects.get(id=2)
                g.user_set.add(user.id)
            elif client.rol == 'US-T':  # USUARIO TRANSPORTE
                g = Group.objects.get(id=3)
                g.user_set.add(user.id)
            elif client.rol == 'US-R':  # USUARIO RESTAURANT
                g = Group.objects.get(id=4)
                g.user_set.add(user.id)
            elif client.rol == 'US-AT':  # USUARIO AGENCIA TURISTICA
                g = Group.objects.get(id=5)
                g.user_set.add(user.id)
            elif client.rol == 'US-ST':  # USUARIO SITIO TURISTICO
                g = Group.objects.get(id=6)
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


@permission_required('tour.change_client', login_url='/accounts/login/')
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


@permission_required('tour.show_client', login_url='/accounts/login/')
def user_show(request, id):
    client = Client.objects.get(id=id)
    a_s = AssignmentSite.objects.filter(client=id)
    a_t = AssignmentTransport.objects.filter(client=id)
    a_a = AssignmentAgency.objects.filter(client=id)
    a_r = AssignmentRestaurant.objects.filter(client=id)
    a_l = AssignmentLodging.objects.filter(client=id)
    return render(request, 'registration/user/show.html', {
        'client': client,
        'a_s': a_s,
        'a_l': a_l,
        'a_t': a_t,
        'a_r': a_r,
        'a_a': a_a,
        'user_obj': Client
    })


@permission_required('tour.delete_client', login_url='/accounts/login/')
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


# PAGINA INICIO ADMINISTRADOR
@login_required
def index_admin(request):
    return render(request, 'admin_page/index.html', {})


# CAMBIO DE LOCALIZACION EN TODA LA PLANTILLA CLIENTE
def change_main(request, id):
    request.session['id_main'] = id
    return HttpResponseRedirect(reverse(index))


# PAGINA INICIO CLIENTE
def index(request):
    restaurants = Restaurant.objects.all
    transports = Transport.objects.all
    agencies = Agency.objects.all
    lodgings = Lodging.objects.all
    socials = Social.objects.all

    return render(request, 'tour/index.html', {
        'restaurants': restaurants,
        'transports': transports,
        'agencies': agencies,
        'lodgings': lodgings,
        'socials': socials
    })


# SECRETARIA CLIENTE
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
    if ids is None or '':
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
    score = round(agency.score / 2)
    return render(request, 'tour/agencies-show.html', {
        'agency': agency,
        'agency_obj': Agency,
        'services': services,
        'schedule': schedule,
        'score': score
    })


# AGENCIAS DE TURISMO ADMINISTRADOR
@permission_required('tour.index_agency', login_url='/accounts/login/')
def agency_index_admin(request):
    if request.user.is_superuser:
        agencies_list = Agency.objects.all()
    else:
        ass = AssignmentAgency.objects.filter(client__user=request.user.id)
        for a in ass:
            agencies_list = Agency.objects.filter(id=a.agency.id)
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


@permission_required('tour.show_agency', login_url='/accounts/login/')
def agency_show_admin(request, id):
    agency = Agency.objects.get(id=id)
    request.session['agency'] = id
    return render(request, 'admin_page/agencies/show.html', {
        'agency': agency,
        'agency_obj': Agency,
    })


@permission_required('tour.add_agency', login_url='/accounts/login/')
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


@permission_required('tour.change_agency', login_url='/accounts/login/')
def agency_active_admin(request, id):
    agency = Agency.objects.get(id=id)
    agency.is_active = True
    save = agency.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('agencies-index-admin'))


@permission_required('tour.change_agency', login_url='/accounts/login/')
def agency_inactive_admin(request, id):
    agency = Agency.objects.get(id=id)
    agency.is_active = False
    save = agency.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('agencies-index-admin'))


@permission_required('tour.change_agency', login_url='/accounts/login/')
def agency_edit_admin(request, id):
    agency = Agency.objects.get(id=id)
    if request.method == 'POST':
        form = AgencyForm(request.POST, request.FILES, instance=agency)
        if form.is_valid():
            save = form.save()
            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('agencies-index-admin', kwargs={'id': agency.id}))
    else:
        form = AgencyForm(instance=agency)
    return render(request, 'admin_page/agencies/edit.html', {
        'agency': agency,
        'form': form,
        'agency_obj': Agency
    })


@permission_required('tour.delete_agency', login_url='/accounts/login/')
def agency_delete_admin(request, id):
    agency = Agency.objects.get(id=id)
    agency.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(agency_index_admin))


# SERVICIOS DE AGENCIAS ADMIN
@permission_required('tour.index_agencyservice', login_url='/accounts/login/')
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


@permission_required('tour.show_agencyservice', login_url='/accounts/login/')
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


@permission_required('tour.add_agencyservice', login_url='/accounts/login/')
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


@permission_required('tour.change_agencyservice', login_url='/accounts/login/')
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


@permission_required('tour.delete_agencyservice', login_url='/accounts/login/')
def agency_service_delete_admin(request, id):
    agency = request.session['agency']
    service = AgencyService.objects.filter(agency=agency).get(id=id)
    service.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('agencies-services-index-admin'))


# HORARIOS DE AGENCIA ADMIN
@permission_required('tour.index_agencyschedule', login_url='/accounts/login/')
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


@permission_required('tour.show_agencyschedule', login_url='/accounts/login/')
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


@permission_required('tour.add_agencyschedule', login_url='/accounts/login/')
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


@permission_required('tour.change_agencyschedule', login_url='/accounts/login/')
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
            return HttpResponseRedirect(reverse('agencies-schedules-index-admin'))
    else:
        form = AgencyScheduleForm(instance=schedule)
    return render(request, 'admin_page/agencies/schedules/edit.html', {
        'schedule': schedule,
        'form': form,
        'schedule_obj': AgencySchedule,
        'agency_title': agency_title,
        'agency_id': agency
    })


@permission_required('tour.delete_agencyschedule', login_url='/accounts/login/')
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
@permission_required('tour.index_event', login_url='/accounts/login/')
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


@permission_required('tour.show_event', login_url='/accounts/login/')
def event_show_admin(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'admin_page/events/show.html', {
        'event': event,
        'event_obj': Event
    })


@permission_required('tour.add_event', login_url='/accounts/login/')
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


@permission_required('tour.change_event', login_url='/accounts/login/')
def event_active_admin(request, id):
    event = Event.objects.get(id=id)
    event.is_active = True
    save = event.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('events-index-admin'))


@permission_required('tour.change_event', login_url='/accounts/login/')
def event_inactive_admin(request, id):
    event = Event.objects.get(id=id)
    event.is_active = False
    save = event.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('events-index-admin'))


@permission_required('tour.change_event', login_url='/accounts/login/')
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


@permission_required('tour.delete_event', login_url='/accounts/login/')
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


# RESTAURANTS ADMIN
@permission_required('tour.index_restaurant', login_url='/accounts/login/')
def restaurant_index_admin(request):
    if request.user.is_superuser:
        restaurants_list = Restaurant.objects.all()
    else:
        ass = AssignmentRestaurant.objects.filter(client__user=request.user.id)
        for a in ass:
            restaurants_list = Restaurant.objects.filter(id=a.restaurant.id)
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


@permission_required('tour.show_restaurant', login_url='/accounts/login/')
def restaurant_show_admin(request, id):
    request.session['restaurants'] = id
    restaurant = Restaurant.objects.get(id=id)
    return render(request, 'admin_page/restaurants/show.html', {
        'restaurant': restaurant,
        'restaurant_obj': Restaurant
    })


@permission_required('tour.add_restaurant', login_url='/accounts/login/')
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


@permission_required('tour.change_restaurant', login_url='/accounts/login/')
def restaurant_active_admin(request, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.is_active = True
    save = restaurant.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('restaurants-index-admin'))


@permission_required('tour.change_restaurant', login_url='/accounts/login/')
def restaurant_inactive_admin(request, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.is_active = False
    save = restaurant.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('restaurants-index-admin'))


@permission_required('tour.change_restaurant', login_url='/accounts/login/')
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


@permission_required('tour.delete_restaurant', login_url='/accounts/login/')
def restaurant_delete_admin(request, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.delete()
    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(restaurant_index_admin))


# MENU DE RESTAURANTES ADMIN
@permission_required('tour.index_restaurantmenu', login_url='/accounts/login/')
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


@permission_required('tour.show_restaurantmenu', login_url='/accounts/login/')
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


@permission_required('tour.add_restaurantmenu', login_url='/accounts/login/')
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


@permission_required('tour.change_restaurantmenu', login_url='/accounts/login/')
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


@permission_required('tour.delete_restaurantmenu', login_url='/accounts/login/')
def restaurant_menu_delete_admin(request, id):
    restaurant = request.session['restaurants']
    menu = RestaurantMenu.objects.filter(restaurant=restaurant).get(id=id)
    menu.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('restaurants-menus-index-admin'))


# HORARIOS DE RESTAURANTES ADMIN
@permission_required('tour.index_restaurantschedule', login_url='/accounts/login/')
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


@permission_required('tour.show_restaurantschedule', login_url='/accounts/login/')
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


@permission_required('tour.add_restaurantschedule', login_url='/accounts/login/')
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


@permission_required('tour.change_restaurantschedule', login_url='/accounts/login/')
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


@permission_required('tour.delete_restaurantschedule', login_url='/accounts/login/')
def restaurant_schedule_delete_admin(request, id):
    restaurant = request.session['restaurants']
    schedule = RestaurantSchedule.objects.filter(restaurant=restaurant).get(id=id)
    schedule.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('restaurants-schedules-index-admin'))


# SERVICIOS DE RESTAURANTES
@permission_required('tour.index_restaurantservice', login_url='/accounts/login/')
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


@permission_required('tour.show_restaurantservice', login_url='/accounts/login/')
def restaurant_service_show_admin(request, id):
    service = RestaurantService.objects.get(id=id)
    return render(request, 'admin_page/restaurants/services/show.html', {
        'service': service,
        'service_obj': RestaurantService,
    })


@permission_required('tour.add_restaurantservice', login_url='/accounts/login/')
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


@permission_required('tour.change_restaurantservice', login_url='/accounts/login/')
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


@permission_required('tour.delete_restaurantservice', login_url='/accounts/login/')
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
@permission_required('tour.index_transport', login_url='/accounts/login/')
def transport_index_admin(request):
    if request.user.is_superuser:
        transports_list = Transport.objects.all()
    else:
        ass = AssignmentTransport.objects.filter(client__user=request.user.id)
        for a in ass:
            transports_list = Transport.objects.filter(id=a.transport.id)
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


@permission_required('tour.show_transport', login_url='/accounts/login/')
def transport_show_admin(request, id):
    transport = Transport.objects.get(id=id)
    request.session['transports'] = id
    destinations = TransportDestination.objects.filter(transport__id=id)
    return render(request, 'admin_page/transports/show.html', {
        'transport': transport,
        'destinations': destinations,
        'transport_obj': Transport
    })


@permission_required('tour.add_transport', login_url='/accounts/login/')
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


@permission_required('tour.change_transport', login_url='/accounts/login/')
def transport_active_admin(request, id):
    transport = Transport.objects.get(id=id)
    transport.is_active = True
    save = transport.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('transports-index-admin'))


@permission_required('tour.change_transport', login_url='/accounts/login/')
def transport_inactive_admin(request, id):
    transport = Transport.objects.get(id=id)
    transport.is_active = False
    save = transport.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('transports-index-admin'))


@permission_required('tour.change_transport', login_url='/accounts/login/')
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


@permission_required('tour.delete_transport', login_url='/accounts/login/')
def transport_delete_admin(request, id):
    transport = Transport.objects.get(id=id)
    transport.delete()
    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(transport_index_admin))


# DESTINOS DE TRANSPORTES
@permission_required('tour.index_transportdestination', login_url='/accounts/login/')
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


@permission_required('tour.show_transportdestination', login_url='/accounts/login/')
def transport_destination_show_admin(request, id):
    transport = request.session['transports']
    request.session['destination'] = id
    return HttpResponseRedirect(reverse(transport_type_service_index_admin))


@permission_required('tour.add_transportdestination', login_url='/accounts/login/')
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


@permission_required('tour.change_transportdestination', login_url='/accounts/login/')
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


@permission_required('tour.delete_transportdestination', login_url='/accounts/login/')
def transport_destination_delete_admin(request, id):
    transport = request.session['transports']
    destination = TransportDestination.objects.filter(transport=transport).get(id=id)
    destination.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('transports-destination-index-admin'))


# SERVICIO DE TRANSPORTES
@permission_required('tour.index_transportservice', login_url='/accounts/login/')
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


@permission_required('tour.show_transportservice', login_url='/accounts/login/')
def transport_service_show_admin(request, id):
    service = TransportService.objects.get(id=id)
    return render(request, 'admin_page/transports/services/show.html', {
        'service': service,
        'service_obj': TransportService,
    })


@permission_required('tour.add_transportservice', login_url='/accounts/login/')
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


@permission_required('tour.change_transportservice', login_url='/accounts/login/')
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


@permission_required('tour.delete_transportservice', login_url='/accounts/login/')
def transport_service_delete_admin(request, id):
    service = TransportService.objects.get(id=id)
    service.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('transports-services-index-admin'))


# TIPO DE SERVICIO DE TRANSPORTES
@permission_required('tour.index_transporttypeservice', login_url='/accounts/login/')
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


@permission_required('tour.show_transporttypeservice', login_url='/accounts/login/')
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


@permission_required('tour.add_transporttypeservice', login_url='/accounts/login/')
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


@permission_required('tour.change_transporttypeservice', login_url='/accounts/login/')
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


@permission_required('tour.delete_transporttypeservice', login_url='/accounts/login/')
def transport_type_service_delete_admin(request, id):
    destination = request.session['destination']
    type_service = TransportTypeService.objects.filter(destination=destination)
    type_service.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('transports-type-services-index-admin'))


# HORARIOS DE TRANSPORTES
@permission_required('tour.index_transportschedule', login_url='/accounts/login/')
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


@permission_required('tour.show_transportschedule', login_url='/accounts/login/')
def transport_schedule_show_admin(request, id):
    transport = request.session['transports']
    schedule = TransportSchedule.objects.filter(transport=transport).get(id=id)
    transport_title = Transport.objects.get(id=transport)
    return render(request, 'admin_page/transports/schedules/show.html', {
        'schedule': schedule,
        'schedule_obj': TransportSchedule,
        'transport_title': transport_title
    })


@permission_required('tour.add_transportschedule', login_url='/accounts/login/')
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


@permission_required('tour.change_transportschedule', login_url='/accounts/login/')
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


@permission_required('tour.delete_transportschedule', login_url='/accounts/login/')
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
@permission_required('tour.index_tourismsite', login_url='/accounts/login/')
def tourism_site_index_admin(request):
    if request.user.is_superuser:
        sites_list = TourismSite.objects.all()
    else:
        ass = AssignmentSite.objects.filter(client__user=request.user.id)
        for a in ass:
            sites_list = TourismSite.objects.filter(id=a.site.id)
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


@permission_required('tour.show_tourismsite', login_url='/accounts/login/')
def tourism_site_show_admin(request, id):
    site = TourismSite.objects.get(id=id)
    request.session['tourism_site'] = id
    return render(request, 'admin_page/tourism_sites/show.html', {
        'site': site,
        'site_obj': TourismSite,
    })


@permission_required('tour.add_tourismsite', login_url='/accounts/login/')
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


@permission_required('tour.change_restaurant', login_url='/accounts/login/')
def tourism_site_active_admin(request, id):
    tourism_site = TourismSite.objects.get(id=id)
    tourism_site.is_active = True
    save = tourism_site.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('tourism_sites-index-admin'))


@permission_required('tour.change_restaurant', login_url='/accounts/login/')
def tourism_site_inactive_admin(request, id):
    tourism_site = TourismSite.objects.get(id=id)
    tourism_site.is_active = False
    save = tourism_site.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('tourism_sites-index-admin'))


@permission_required('tour.change_tourismsite', login_url='/accounts/login/')
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


@permission_required('tour.delete_tourismsite', login_url='/accounts/login/')
def tourism_site_delete_admin(request, id):
    tourism_site = TourismSite.objects.get(id=id)
    tourism_site.delete()
    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(tourism_site_index_admin))


# MENU DE SITIOS TURISTICOS
@permission_required('tour.index_tourismsitemenu', login_url='/accounts/login/')
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


@permission_required('tour.show_tourismsitemenu', login_url='/accounts/login/')
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


@permission_required('tour.new_tourismsitemenu', login_url='/accounts/login/')
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


@permission_required('tour.edit_tourismsitemenu', login_url='/accounts/login/')
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


@permission_required('tour.delete_tourismsitemenu', login_url='/accounts/login/')
def tourism_site_menu_delete_admin(request, id):
    tourism_site = request.session['tourism_site']
    menu = TourismSiteMenu.objects.filter(site=tourism_site).get(id=id)
    menu.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('tourism_sites-menus-index-admin'))


# HORARIOS DE SITIOS TURISTICOS
@permission_required('tour.index_tourismsiteschedule', login_url='/accounts/login/')
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


@permission_required('tour.show_tourismsiteschedule', login_url='/accounts/login/')
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


@permission_required('tour.add_tourismsiteschedule', login_url='/accounts/login/')
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


@permission_required('tour.change_tourismsiteschedule', login_url='/accounts/login/')
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


@permission_required('tour.delete_tourismsiteschedule', login_url='/accounts/login/')
def tourism_site_schedule_delete_admin(request, id):
    tourism_site = request.session['tourism_site']
    schedule = TourismSiteSchedule.objects.filter(site=tourism_site).get(id=id)
    schedule.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('tourism_sites-schedules-index-admin'))


# TIPOS DE SITIOS TURISTICOS
@permission_required('tour.index_tourismsitetype', login_url='/accounts/login/')
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


@permission_required('tour.show_tourismsitetype', login_url='/accounts/login/')
def tourism_site_type_show_admin(request, id):
    type = TourismSiteType.objects.get(id=id)
    return render(request, 'admin_page/tourism_sites/types/show.html', {
        'type': type,
        'type_obj': TourismSiteType,
    })


@permission_required('tour.add_tourismsitetype', login_url='/accounts/login/')
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


@permission_required('tour.change_tourismsitetype', login_url='/accounts/login/')
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


@permission_required('tour.delete_tourismsitetype', login_url='/accounts/login/')
def tourism_site_type_delete_admin(request, id):
    type = TourismSiteType.objects.get(id=id)
    type.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('tourism_sites-types-index-admin'))


# SERVICIOS DE SITIOS TURISTICOS
@permission_required('tour.index_tourismsiteservice', login_url='/accounts/login/')
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


@permission_required('tour.show_tourismsiteservice', login_url='/accounts/login/')
def tourism_site_service_show_admin(request, id):
    service = TourismSiteService.objects.get(id=id)
    return render(request, 'admin_page/tourism_sites/services/show.html', {
        'service': service,
        'service_obj': TourismSiteService,
    })


@permission_required('tour.add_tourismsiteservice', login_url='/accounts/login/')
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


@permission_required('tour.change_tourismsiteservice', login_url='/accounts/login/')
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


@permission_required('tour.delete_tourismsiteservice', login_url='/accounts/login/')
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
@permission_required('tour.index_tourismroute', login_url='/accounts/login/')
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


@permission_required('tour.show_tourismroute', login_url='/accounts/login/')
def tourism_route_show_admin(request, id):
    request.session['tourism_route'] = id
    route = TourismRoute.objects.get(id=id)
    return render(request, 'admin_page/tourism_routes/show.html', {
        'route': route,
        'route_obj': TourismRoute
    })


@permission_required('tour.add_tourismroute', login_url='/accounts/login/')
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


@permission_required('tour.change_tourism_route', login_url='/accounts/login/')
def tourism_route_active_admin(request, id):
    route = TourismRoute.objects.get(id=id)
    route.is_active = True
    save = route.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('tourism_routes-index-admin'))


@permission_required('tour.change_tourism_route', login_url='/accounts/login/')
def tourism_route_inactive_admin(request, id):
    route = TourismRoute.objects.get(id=id)
    route.is_active = False
    save = route.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('tourism_routes-index-admin'))


@permission_required('tour.change_tourismroute', login_url='/accounts/login/')
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


@permission_required('tour.delete_tourismroute', login_url='/accounts/login/')
def tourism_route_delete_admin(request, id):
    route = TourismRoute.objects.get(id=id)
    route.delete()
    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(tourism_route_index_admin))


# MENU DE RUTAS TURISTICAS
@permission_required('tour.index_tourismroutemenu', login_url='/accounts/login/')
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


@permission_required('tour.show_tourismroutemenu', login_url='/accounts/login/')
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


@permission_required('tour.add_tourismroutemenu', login_url='/accounts/login/')
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


@permission_required('tour.change_tourismroutemenu', login_url='/accounts/login/')
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


@permission_required('tour.delete_tourismroutemenu', login_url='/accounts/login/')
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
@permission_required('tour.index_lodging', login_url='/accounts/login/')
def lodging_index_admin(request):
    if request.user.is_superuser:
        lodgings_list = Lodging.objects.all()
    else:
        ass = AssignmentLodging.objects.filter(client__user=request.user.id)
        for a in ass:
            lodgings_list = Lodging.objects.filter(id=a.lodging.id)
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


@permission_required('tour.show_lodging', login_url='/accounts/login/')
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


@permission_required('tour.add_lodging', login_url='/accounts/login/')
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


@permission_required('tour.change_lodging', login_url='/accounts/login/')
def lodging_active_admin(request, id):
    lodging = Lodging.objects.get(id=id)
    lodging.is_active = True
    save = lodging.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('lodgings-index-admin'))


@permission_required('tour.change_lodging', login_url='/accounts/login/')
def lodging_inactive_admin(request, id):
    lodging = Lodging.objects.get(id=id)
    lodging.is_active = False
    save = lodging.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('lodgings-index-admin'))


@permission_required('tour.change_lodging', login_url='/accounts/login/')
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


@permission_required('tour.delete_lodging', login_url='/accounts/login/')
def lodging_delete_admin(request, id):
    lodging = Lodging.objects.get(id=id)
    lodging.delete()
    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse(lodging_index_admin))


# CUARTOS DE HOSPEDAJES
@permission_required('tour.index_lodgingroom', login_url='/accounts/login/')
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


@permission_required('tour.show_lodgingroom', login_url='/accounts/login/')
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


@permission_required('tour.add_lodgingroom', login_url='/accounts/login/')
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


@permission_required('tour.change_lodgingroom', login_url='/accounts/login/')
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


@permission_required('tour.delete_lodgingroom', login_url='/accounts/login/')
def lodging_room_delete_admin(request, id):
    lodging = request.session['lodgings']
    room = LodgingRoom.objects.filter(lodging=lodging).get(id=id)
    room.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('lodgings-room-index-admin'))


# HORARIOS DE HOSPEDAJES
@permission_required('tour.index_lodgingschedule', login_url='/accounts/login/')
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


@permission_required('tour.show_lodgingschedule', login_url='/accounts/login/')
def lodging_schedule_show_admin(request, id):
    lodging = request.session['lodgings']
    schedule = LodgingSchedule.objects.filter(lodging=lodging).get(id=id)
    lodging_title = Lodging.objects.get(id=lodging)
    return render(request, 'admin_page/lodgings/schedules/show.html', {
        'schedule': schedule,
        'schedule_obj': LodgingSchedule,
        'lodging_title': lodging_title
    })


@permission_required('tour.add_lodgingschedule', login_url='/accounts/login/')
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


@permission_required('tour.change_lodgingschedule', login_url='/accounts/login/')
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
            return HttpResponseRedirect(reverse('lodgings-schedules-index-admin'))
    else:
        form = LodgingScheduleForm(instance=schedule)
    return render(request, 'admin_page/lodgings/schedules/edit.html', {
        'schedule': schedule,
        'form': form,
        'schedule_obj': LodgingSchedule,
        'lodging_title': lodging_title,
        'lodging_id': lodging
    })


@permission_required('tour.delete_lodgingschedule', login_url='/accounts/login/')
def lodging_schedule_delete_admin(request, id):
    lodging = request.session['lodgings']
    schedule = LodgingSchedule.objects.filter(lodging=lodging).get(id=id)
    schedule.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('lodgings-schedules-index-admin'))


# TIPOS DE HOSPEDAJES
@permission_required('tour.index_lodgingtype', login_url='/accounts/login/')
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


@permission_required('tour.show_lodgingtype', login_url='/accounts/login/')
def lodging_type_show_admin(request, id):
    type = LodgingType.objects.get(id=id)
    return render(request, 'admin_page/lodgings/types/show.html', {
        'type': type,
        'type_obj': LodgingType,
    })


@permission_required('tour.add_lodgingtype', login_url='/accounts/login/')
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


@permission_required('tour.change_lodgingtype', login_url='/accounts/login/')
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


@permission_required('tour.delete_lodgingtype', login_url='/accounts/login/')
def lodging_type_delete_admin(request, id):
    type = LodgingType.objects.get(id=id)
    type.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('lodgings-types-index-admin'))


# SERVICIOS DE HOSPEDAJES
@permission_required('tour.index_lodgingservice', login_url='/accounts/login/')
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


@permission_required('tour.show_lodgingservice', login_url='/accounts/login/')
def lodging_service_show_admin(request, id):
    service = LodgingService.objects.get(id=id)
    return render(request, 'admin_page/lodgings/services/show.html', {
        'service': service,
        'service_obj': LodgingService,
    })


@permission_required('tour.add_lodgingservice', login_url='/accounts/login/')
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


@permission_required('tour.change_lodgingservice', login_url='/accounts/login/')
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


@permission_required('tour.delete_lodgingservice', login_url='/accounts/login/')
def lodging_service_delete_admin(request, id):
    service = LodgingService.objects.get(id=id)
    service.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('lodgings-services-index-admin'))


# LOCALIZACIONES
@permission_required('tour.index_location', login_url='/accounts/login/')
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


@permission_required('tour.show_location', login_url='/accounts/login/')
def location_show_admin(request, id):
    destination = Location.objects.get(id=id)
    return render(request, 'admin_page/locations/show.html', {
        'destination': destination,
        'destination_obj': Location,
    })


@permission_required('tour.add_location', login_url='/accounts/login/')
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


@permission_required('tour.change_location', login_url='/accounts/login/')
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


@permission_required('tour.delete_location', login_url='/accounts/login/')
def location_delete_admin(request, id):
    destination = Location.objects.get(id=id)
    destination.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('location-index-admin'))


# CONFIGURACIONES
@permission_required('tour.index_objective', login_url='/accounts/login/')
def configuration_index(request):
    objectives = Objective.objects.all
    secretaries = Secretary.objects.all
    laws = Law.objects.all
    functions = Function.objects.all
    socials = Social.objects.all
    return render(request, 'admin_page/configurations/index.html', {
        'objectives': objectives,
        'secretaries': secretaries,
        'laws': laws,
        'functions': functions,
        'socials': socials,
    })


# OBJETIVOS
@permission_required('tour.add_objective', login_url='/accounts/login/')
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


@permission_required('tour.change_objective', login_url='/accounts/login/')
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


@permission_required('tour.delete_objective', login_url='/accounts/login/')
def objective_delete(request, id):
    objective = Objective.objects.get(id=id)
    objective.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('configurations-index'))


# FUNCIONES
@permission_required('tour.add_function', login_url='/accounts/login/')
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


@permission_required('tour.change_function', login_url='/accounts/login/')
def function_active_admin(request, id):
    function = Function.objects.get(id=id)
    function.is_active = True
    save = function.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('configurations-index'))


@permission_required('tour.change_function', login_url='/accounts/login/')
def function_inactive_admin(request, id):
    function = Function.objects.get(id=id)
    function.is_active = False
    save = function.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('configurations-index'))


@permission_required('tour.change_function', login_url='/accounts/login/')
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


@permission_required('tour.delete_function', login_url='/accounts/login/')
def function_delete(request, id):
    function = Function.objects.get(id=id)
    function.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('configurations-index'))


# LEYES
@permission_required('tour.add_law', login_url='/accounts/login/')
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


@permission_required('tour.change_law', login_url='/accounts/login/')
def law_active_admin(request, id):
    law = Law.objects.get(id=id)
    law.is_active = True
    save = law.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('configurations-index'))


@permission_required('tour.change_law', login_url='/accounts/login/')
def law_inactive_admin(request, id):
    law = Law.objects.get(id=id)
    law.is_active = False
    save = law.save()

    message = "actualizado Correctamente"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('configurations-index'))


@permission_required('tour.change_law', login_url='/accounts/login/')
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


@permission_required('tour.delete_law', login_url='/accounts/login/')
def law_delete(request, id):
    law = Law.objects.get(id=id)
    law.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('configurations-index'))


# SECRETARIO
@permission_required('tour.add_secretary', login_url='/accounts/login/')
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


@permission_required('tour.change_secretary', login_url='/accounts/login/')
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


@permission_required('tour.delete_secretary', login_url='/accounts/login/')
def secretary_delete(request, id):
    secretary = Secretary.objects.get(id=id)
    secretary.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('configurations-index'))


# REDES SOCIALES
@permission_required('tour.add_social', login_url='/accounts/login/')
def social_new(request):
    if request.method == 'POST':
        form = SocialForm(request.POST, request.FILES)
        if form.is_valid():
            social = form.save(commit=False)
            social.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('configurations-index'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = SocialForm()
    return render(request, 'admin_page/configurations/socials/new.html', {
        'form': form,
    })


@permission_required('tour.change_social', login_url='/accounts/login/')
def social_edit(request, id):
    social = Social.objects.get(id=id)
    if request.method == 'POST':
        form = SocialForm(request.POST, request.FILES, instance=social)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('configurations-index'))
    else:
        form = SocialForm(instance=social)
    return render(request, 'admin_page/configurations/socials/edit.html', {
        'social': social,
        'form': form,
        'social_obj': Social
    })


@permission_required('tour.delete_social', login_url='/accounts/login/')
def social_delete(request, id):
    social = Social.objects.get(id=id)
    social.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('configurations-index'))


# ASIGNACIONES
@permission_required('tour.index_assignment_site', login_url='/accounts/login/')
def assignments_index(request):
    lodgings = AssignmentLodging.objects.all
    restaurants = AssignmentRestaurant.objects.all
    agencies = AssignmentAgency.objects.all
    transports = AssignmentTransport.objects.all
    sites = AssignmentSite.objects.all
    return render(request, 'admin_page/assignments/index.html', {
        'lodgings': lodgings,
        'restaurants': restaurants,
        'agencies': agencies,
        'transports': transports,
        'sites': sites,
    })


# ASSIGNACION DE SITIOS TURISTICOS
@permission_required('tour.add_assignment_site', login_url='/accounts/login/')
def assignment_site_new(request):
    if request.method == 'POST':
        form = AssignmentSiteForm(request.POST, request.FILES)
        if form.is_valid():
            assignment_site = form.save(commit=False)
            assignment_site.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('assignments-index'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = AssignmentSiteForm()
    return render(request, 'admin_page/assignments/assignment_sites/new.html', {
        'form': form,
    })


@permission_required('tour.change_assignment_site', login_url='/accounts/login/')
def assignment_site_edit(request, id):
    assignment_site = AssignmentSite.objects.get(id=id)
    if request.method == 'POST':
        form = AssignmentSiteForm(request.POST, request.FILES, instance=assignment_site)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('assignments-index'))
    else:
        form = AssignmentSiteForm(instance=assignment_site)
    return render(request, 'admin_page/assignments/assignment_sites/edit.html', {
        'assignment_site': assignment_site,
        'form': form,
        'assignment_site_obj': AssignmentSite
    })


@permission_required('tour.delete_assignment_site', login_url='/accounts/login/')
def assignment_site_delete(request, id):
    assignment_site = AssignmentSite.objects.get(id=id)
    assignment_site.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('assignments-index'))


# ASSIGNACION DE TRANSPORTES
@permission_required('tour.add_assignment_transport', login_url='/accounts/login/')
def assignment_transport_new(request):
    if request.method == 'POST':
        form = AssignmentTransportForm(request.POST, request.FILES)
        if form.is_valid():
            assignment_transport = form.save(commit=False)
            assignment_transport.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('assignments-index'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = AssignmentTransportForm()
    return render(request, 'admin_page/assignments/assignment_transports/new.html', {
        'form': form,
    })


@permission_required('tour.change_assignment_transport', login_url='/accounts/login/')
def assignment_transport_edit(request, id):
    assignment_transport = AssignmentTransport.objects.get(id=id)
    if request.method == 'POST':
        form = AssignmentTransportForm(request.POST, request.FILES, instance=assignment_transport)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('assignments-index'))
    else:
        form = AssignmentTransportForm(instance=assignment_transport)
    return render(request, 'admin_page/assignments/assignment_transports/edit.html', {
        'assignment_transport': assignment_transport,
        'form': form,
        'assignment_transport_obj': AssignmentTransport
    })


@permission_required('tour.delete_assignment_transport', login_url='/accounts/login/')
def assignment_transport_delete(request, id):
    assignment_transport = AssignmentTransport.objects.get(id=id)
    assignment_transport.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('assignments-index'))


# ASSIGNACION DE RESTAURANTES
@permission_required('tour.add_assignment_restaurant', login_url='/accounts/login/')
def assignment_restaurant_new(request):
    if request.method == 'POST':
        form = AssignmentRestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            assignment_restaurant = form.save(commit=False)
            assignment_restaurant.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('assignments-index'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = AssignmentRestaurantForm()
    return render(request, 'admin_page/assignments/assignment_restaurants/new.html', {
        'form': form,
    })


@permission_required('tour.change_assignment_restaurant', login_url='/accounts/login/')
def assignment_restaurant_edit(request, id):
    assignment_restaurant = AssignmentRestaurant.objects.get(id=id)
    if request.method == 'POST':
        form = AssignmentRestaurantForm(request.POST, request.FILES, instance=assignment_restaurant)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('assignments-index'))
    else:
        form = AssignmentRestaurantForm(instance=assignment_restaurant)
    return render(request, 'admin_page/assignments/assignment_restaurants/edit.html', {
        'assignment_restaurant': assignment_restaurant,
        'form': form,
        'assignment_restaurant_obj': AssignmentRestaurant
    })


@permission_required('tour.delete_assignment_restaurant', login_url='/accounts/login/')
def assignment_restaurant_delete(request, id):
    assignment_restaurant = AssignmentRestaurant.objects.get(id=id)
    assignment_restaurant.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('assignments-index'))


# ASSIGNACION DE AGENCIAS
@permission_required('tour.add_assignment_agency', login_url='/accounts/login/')
def assignment_agency_new(request):
    if request.method == 'POST':
        form = AssignmentAgencyForm(request.POST, request.FILES)
        if form.is_valid():
            assignment_agency = form.save(commit=False)
            assignment_agency.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('assignments-index'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = AssignmentAgencyForm()
    return render(request, 'admin_page/assignments/assignment_agencys/new.html', {
        'form': form,
    })


@permission_required('tour.change_assignment_agency', login_url='/accounts/login/')
def assignment_agency_edit(request, id):
    assignment_agency = AssignmentAgency.objects.get(id=id)
    if request.method == 'POST':
        form = AssignmentAgencyForm(request.POST, request.FILES, instance=assignment_agency)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('assignments-index'))
    else:
        form = AssignmentAgencyForm(instance=assignment_agency)
    return render(request, 'admin_page/assignments/assignment_agencys/edit.html', {
        'assignment_agency': assignment_agency,
        'form': form,
        'assignment_agency_obj': AssignmentAgency
    })


@permission_required('tour.delete_assignment_agency', login_url='/accounts/login/')
def assignment_agency_delete(request, id):
    assignment_agency = AssignmentAgency.objects.get(id=id)
    assignment_agency.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('assignments-index'))


# ASSIGNACION DE SITIOS TURISTICOS
@permission_required('tour.add_assignment_lodging', login_url='/accounts/login/')
def assignment_lodging_new(request):
    if request.method == 'POST':
        form = AssignmentLodgingForm(request.POST, request.FILES)
        if form.is_valid():
            assignment_lodging = form.save(commit=False)
            assignment_lodging.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('assignments-index'))
        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = AssignmentLodgingForm()
    return render(request, 'admin_page/assignments/assignment_lodgings/new.html', {
        'form': form,
    })


@permission_required('tour.change_assignment_lodging', login_url='/accounts/login/')
def assignment_lodging_edit(request, id):
    assignment_lodging = AssignmentLodging.objects.get(id=id)
    if request.method == 'POST':
        form = AssignmentLodgingForm(request.POST, request.FILES, instance=assignment_lodging)
        if form.is_valid():
            save = form.save()

            message = "actualizado Correctamente"
            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(reverse('assignments-index'))
    else:
        form = AssignmentLodgingForm(instance=assignment_lodging)
    return render(request, 'admin_page/assignments/assignment_lodgings/edit.html', {
        'assignment_lodging': assignment_lodging,
        'form': form,
        'assignment_lodging_obj': AssignmentLodging
    })


@permission_required('tour.delete_assignment_lodging', login_url='/accounts/login/')
def assignment_lodging_delete(request, id):
    assignment_lodging = AssignmentLodging.objects.get(id=id)
    assignment_lodging.delete()

    message = 'Eliminado!'
    messages.add_message(request, messages.SUCCESS, message)

    return HttpResponseRedirect(reverse('assignments-index'))
