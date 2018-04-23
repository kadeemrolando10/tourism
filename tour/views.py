from django.shortcuts import render
from tour.forms import EventForm
from tour.models import Event, Restaurant, Tourism_site, Transport, Lodgment, Agency, Service_Transport, Service_Agency
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
        return render(request, 'tour/index.html', {})


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


def transport_index(request):
    transports = Transport.objects.all
    return render(request, 'tour/transports-index.html', {
        'transports': transports,
        'transport_obj': Transport
    })


def torism_site_index(request):
    tourism_sites = Restaurant.objects.all
    return render(request, 'tour/tourism_sites-index.html', {
        'tourism_sites': tourism_sites,
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

