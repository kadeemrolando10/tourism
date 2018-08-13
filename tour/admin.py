from django.contrib import admin

from tour.models import LodgingSchedule, TourismRoute, Location, TourismRouteMenu, Event, Transport, Agency, \
    TourismSite, Restaurant, Lodging, LodgingType, \
    TransportService, LodgingService, AgencyService, RestaurantService, Function, Objective, \
    RestaurantMenu, TransportDestination, TransportTypeService, \
    LodgingRoom, TourismSiteService, TourismSiteType, TourismSiteMenu, AgencySchedule, \
    TransportSchedule, TourismSiteSchedule, RestaurantSchedule, Secretary, Law

admin.site.register(TourismSiteType)
admin.site.register(TourismSiteMenu)
admin.site.register(TourismSiteService)
admin.site.register(Location)
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
admin.site.register(Objective)
admin.site.register(Function)
admin.site.register(Secretary)
admin.site.register(Law)
