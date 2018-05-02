from django.shortcuts import render
from tour.forms import EventForm
from tour.models import Event, Restaurant, Tourism_site, Transport, Lodgment, Agency, Objetive, Function,Document
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
    events = Event.objects.all
    restaurants = Restaurant.objects.all
    transports = Transport.objects.all
    tourism_sites = Restaurant.objects.all
    agencys = Agency.objects.all
    lodgments = Lodgment.objects.all
    return render(request, 'tour/index.html', {
        'events': events,
        'restaurants': restaurants,
        'transports': transports,
        'tourism_sites': tourism_sites,
        'agencys': agencys,
        'lodgments': lodgments,
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
    restaurants = Restaurant.objects.all
    return render(request, 'tour/restaurants-show.html', {
        'restaurant': restaurant,
        'restaurants': restaurants,
        'restaurant_obj': Restaurant
    })


def transport_index(request):
    transports = Transport.objects.all
    return render(request, 'tour/transports-index.html', {
        'transports': transports,
        'transport_obj': Transport
    })


def torism_site_index(request):
    tourism_sites = Tourism_site.objects.all
    return render(request, 'tour/tourism_sites-index.html', {
        'tourism': tourism_sites,
        'tourism_site_obj': Tourism_site
    })


def agency_index(request):
    agencys = Agency.objects.all
    return render(request, 'tour/agencys-index.html', {
        'agencys': agencys,
        'agency_obj': Agency,
    })


def lodgment_index(request):
    lodgments = Lodgment.objects.all
    return render(request, 'tour/lodgments-index.html', {
        'lodgments': lodgments,
        'lodgment_obj': Lodgment
    })

