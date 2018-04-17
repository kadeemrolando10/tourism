from django.contrib import admin
from .models import Event, Transport,Agency,Tourism_site,Restaurant,Lodgment,Lodgment_type,\
                    Service_Transport,Service_Lodgment,Service_Agency,Service_Restaurant

admin.site.register(Event)
admin.site.register(Transport)
admin.site.register(Tourism_site)
admin.site.register(Agency)
admin.site.register(Restaurant)
admin.site.register(Lodgment_type)
admin.site.register(Lodgment)
admin.site.register(Service_Restaurant)
admin.site.register(Service_Agency)
admin.site.register(Service_Transport)
admin.site.register(Service_Lodgment)