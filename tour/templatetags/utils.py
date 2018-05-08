# encoding:utf-8
from django import template
from django.apps import apps

from tour.models import TransportService
from tour.models import TransportTypeService
from tour.models import TransportDestination
from tour.models import TourismSiteType
from tour.models import TourismSite
from tour.models import Lodging
register = template.Library()


@register.filter()
def to_int(value):
    return int(value)


@register.simple_tag
def get_services(id):
    id = int(id)
    return TransportService.objects.filter(type_id=id)


@register.simple_tag
def get_typeservices(id):
    id = int(id)
    return TransportTypeService.objects.filter(destination_id=id).order_by('price')


@register.simple_tag
def get_typeservicest(id):
    id = int(id)
    return TourismSiteType.objects.filter(destination=id)


@register.simple_tag
def get_servicest(id):
    id = int(id)
    return TourismSite.objects.filter(type=id)


@register.simple_tag
def get_lodging(id):
    id = int(id)
    return Lodging.objects.filter(type=id)


@register.simple_tag
def get_destiny_transport(id):
    id = int(id)
    return TransportDestination.objects.filter(transport=id)


@register.simple_tag
def get_response_value(diagnose, formdiagnose, q):
    pass


