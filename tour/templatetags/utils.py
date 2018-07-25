# encoding:utf-8
from django import template
from django.apps import apps

from tour.models import TransportService, DAYS, TourismRoute, TourismRouteMenu, ROLE_USERS, GENDER
from tour.models import TransportTypeService
from tour.models import TransportDestination
from tour.models import TourismSiteType
from tour.models import TourismSiteMenu
from tour.models import TourismSite
from tour.models import Lodging

register = template.Library()


@register.filter()
def to_int(value):
    return int(value)


@register.simple_tag
def get_days(day):
    for date in DAYS:
        if date[0] == day:
            return date[1]
    return None


@register.simple_tag
def get_destiny_transport(id):
    id = int(id)
    return TransportDestination.objects.filter(transport=id)


@register.simple_tag
def get_field_name(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name.title()


@register.simple_tag
def get_field_name_schedule(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name.day()


@register.simple_tag
def is_image(value):
    if (value.name.endswith('.png') or
            value.name.endswith('.jpg') or
            value.name.endswith('.gif') or
            value.name.endswith('.bmp')):
        return True
    else:
        return False


@register.simple_tag
def get_types_services_transport(id):
    id = int(id)
    return TransportTypeService.objects.filter(destination_id=id).order_by('price')


@register.simple_tag
def get_lodging(id):
    id = int(id)
    return Lodging.objects.filter(type=id)


@register.simple_tag
def get_type_tourism_site(id):
    id = int(id)
    return TourismSiteType.objects.filter(destination=id)


@register.simple_tag
def get_tourism_route(id):
    id = int(id)
    return TourismRoute.objects.filter(destination=id)


@register.simple_tag
def get_tourism_site(id):
    id = int(id)
    return TourismSite.objects.filter(destination=id)


@register.simple_tag
def get_tourism_site_menu(id):
    id = int(id)
    return TourismSiteMenu.objects.filter(site=id)


@register.simple_tag
def get_tourism_route_menu(id):
    id = int(id)
    return TourismRouteMenu.objects.filter(route=id)


@register.simple_tag
def get_gender_user(gender):
    for status in GENDER:
        if status[0] == gender:
            return status[1]
    return None


@register.simple_tag
def get_role_user(rol):
    for status in ROLE_USERS:
        if status[0] == rol:
            return status[1]
    return None

@register.filter(name='times')
def times(number):
    return range(number)

@register.simple_tag
def get_response_value(diagnose, formdiagnose, q):
    pass
