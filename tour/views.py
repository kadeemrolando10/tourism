from django.shortcuts import render
from tour.forms import EventForm
from tour.models import Event, Restaurant, TourismSite, Transport, Lodging, Agency, Objetive, Function, Document, \
    TransportDestination, TransportTypeService, TransportService, LodgingService, LodgingRoom, LodgingType, \
    TourismSiteDestiny
from tour.forms import RestaurantForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
    events = Event.objects.all
    restaurants = Restaurant.objects.all
    transports = Transport.objects.all
    tourism_sites = Restaurant.objects.all
    agencys = Agency.objects.all
    lodging = Lodging.objects.all
    return render(request, 'tour/index.html', {
        'events': events,
        'restaurants': restaurants,
        'transports': transports,
        'tourism_sites': tourism_sites,
        'agencys': agencys,
        'lodging': lodging,
    })


def secretary(request):
    obj = Objetive.objects.all
    func = Function.objects.all
    doc = Document.objects.all
    return render(request, 'tour/secretary.html', {
        'objetivos': obj,
        'funciones': func,
        'documento': doc
    })


def event_index(request):
    events = Event.objects.all
    return render(request, 'tour/events-index.html', {
        'events': events,
        'event_obj': Event
    })


def restaurant_index(request):
    restaurants = Restaurant.objects.all
    return render(request, 'tour/restaurants-index.html', {
        'restaurants': restaurants,
        'restaurant_obj': Restaurant
    })


def restaurant_show(request, id):
    restaurant = Restaurant.objects.get(id=id)
    return render(request, 'tour/restaurants-show.html', {
        'restaurant': restaurant,
        'restaurant_obj': Restaurant
    })


def restaurant_new(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.save()

            message = 'Registrado correctamente!'
            messages.add_message(request, messages.SUCCESS, message)
            return HttpResponseRedirect(reverse('restaurants-show', kwargs={'id': restaurant.id}))

        else:
            message = 'Existen errores por favor verifica!.'
            messages.add_message(request, messages.ERROR, message)
    else:
        form = RestaurantForm()
    return render(request, 'tour/restaurants-new.html', {'form': form})


def transport_index(request):
    transports = Transport.objects.all
    return render(request, 'tour/transports-index.html', {
        'transports': transports,
        'transport_obj': Transport
    })


def transport_show(request, id):
    transport = Transport.objects.get(id=id)
    destinations = TransportDestination.objects.filter(transport__id=id)
    return render(request, 'tour/transports-show.html', {
        'transport': transport,
        'destinations': destinations,
        'transport_obj': Transport
    })


def tourism_site_index(request):
    tourism_sites = TourismSite.objects.all
    return render(request, 'tour/tourism_sites-index.html', {
        'tourism': tourism_sites,
        'tourism_site_obj': TourismSite
    })


def tourism_site_show(request, id):
    site = TourismSite.objects.get(id=id)
    destinations = TourismSiteDestiny.objects.all
    return render(request, 'tour/tourism_site-show.html', {
        'site': site,
        'destinations': destinations,
    })


def agency_index(request):
    agencys = Agency.objects.all
    return render(request, 'tour/agencys-index.html', {
        'agencys': agencys,
        'agency_obj': Agency,
    })


def lodging_index(request):
    typeslod = LodgingType.objects.all
    return render(request, 'tour/lodging-index.html', {
        'typeslod': typeslod,
        'lodging_obj': Lodging
    })


def lodging_show(request, id):
    lod = Lodging.objects.get(id=id)
    room = LodgingRoom.objects.filter(lodging=id).order_by('price')
    return render(request, 'tour/lodging-show.html', {
        'lodging': lod,
        'room': room,
        'lodging_obj': Lodging
    })
