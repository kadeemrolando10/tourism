from django.contrib import admin
from .models import Event, Transport, Agency, TourismSite, Restaurant, Lodging, LodgingType, \
    TransportService, LodgingService, AgencyService, RestaurantService, Function, Objective, Document, \
    RestaurantMenu, Schedule, TransportDestination, TransportTypeService, \
    LodgingRoom, TourismSiteDestiny, TourismSiteService, TourismSiteType, TourismSiteMenu

admin.site.register(TourismSiteType)
admin.site.register(TourismSiteMenu)
admin.site.register(TourismSiteService)
admin.site.register(TourismSiteDestiny)
admin.site.register(Objective)
admin.site.register(Function)
admin.site.register(Event)
admin.site.register(Transport)
admin.site.register(TourismSite)
admin.site.register(Agency)
admin.site.register(Restaurant)
admin.site.register(LodgingService)
admin.site.register(LodgingRoom)
admin.site.register(Lodging)
admin.site.register(RestaurantService)
admin.site.register(AgencyService)
admin.site.register(TransportService)
admin.site.register(LodgingType)
admin.site.register(Document)
admin.site.register(RestaurantMenu)
admin.site.register(Schedule)
admin.site.register(TransportDestination)
admin.site.register(TransportTypeService)
