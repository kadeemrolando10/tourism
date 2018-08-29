# encoding:utf-8
import logging
from django import template

from tour.models import DAYS, TourismRoute, TourismRouteMenu, ROLE_USERS, GENDER, MENU, Location, Transport, Restaurant, \
    Agency, Social
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


@register.simple_tag()
def get_user_groups(r):
    return r.user.groups.all()


@register.simple_tag()
def get_quantity_notify():
    s = TourismSite.objects.filter(is_active=False)
    t = Transport.objects.filter(is_active=False)
    r = Restaurant.objects.filter(is_active=False)
    a = Agency.objects.filter(is_active=False)
    l = Lodging.objects.filter(is_active=False)
    cont = s.count() + r.count() + t.count() + a.count() + l.count()
    return cont


@register.simple_tag
def get_notify_sites():
    sites = TourismSite.objects.filter(is_active=False)
    return sites


@register.simple_tag
def get_notify_transports():
    transports = Transport.objects.filter(is_active=False)
    return transports


@register.simple_tag
def get_notify_restaurants():
    restaurants = Restaurant.objects.filter(is_active=False)
    return restaurants


@register.simple_tag
def get_notify_agencies():
    agencies = Agency.objects.filter(is_active=False)
    return agencies


@register.simple_tag
def get_notify_lodgings():
    lodgings = Lodging.objects.filter(is_active=False)
    return lodgings


@register.simple_tag
def get_days(day):
    for date in DAYS:
        if date[0] == day:
            return date[1]
    return None


@register.simple_tag
def get_category(category):
    for categories in MENU:
        if categories[0] == category:
            return categories[1]
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
def get_locations():
    return Location.objects.all


@register.simple_tag
def get_socials():
    return Social.objects.all


@register.simple_tag
def get_location(id):
    id = int(id)
    return Location.objects.get(id=id)


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
def get_rounded(score):
    logging.info(score)
    return round(score / 2)


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
