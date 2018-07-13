from django.contrib import admin

from tour.models import LodgingSchedule, TourismRoute, TourismRouteDestiny, TourismRouteMenu, Event, Transport, Agency,\
    TourismSite, Restaurant, Lodging, LodgingType, \
    TransportService, LodgingService, AgencyService, RestaurantService, Function, Objective, Document, \
    RestaurantMenu, TransportDestination, TransportTypeService, \
    LodgingRoom, TourismSiteDestiny, TourismSiteService, TourismSiteType, TourismSiteMenu, AgencySchedule, \
    TransportSchedule, TourismSiteSchedule, RestaurantSchedule

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
admin.site.register(TransportDestination)
admin.site.register(TransportTypeService)
admin.site.register(TransportSchedule)
admin.site.register(TourismSiteSchedule)
admin.site.register(AgencySchedule)
admin.site.register(LodgingSchedule)
admin.site.register(RestaurantSchedule)
admin.site.register(TourismRoute)
admin.site.register(TourismRouteMenu)
admin.site.register(TourismRouteDestiny)
