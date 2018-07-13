from django import forms
from django.forms import CheckboxSelectMultiple

from tour_site.services import BaseForm
from tour.models import Event, Restaurant, TourismSite, Transport, Lodging, Agency, TourismRoute, AgencyService, \
    AgencySchedule, RestaurantService, RestaurantSchedule, RestaurantMenu, TransportDestination, TransportService, \
    TransportTypeService, TransportSchedule, TourismSiteMenu, TourismSiteSchedule, TourismSiteDestiny, TourismSiteType, \
    TourismSiteService, TourismRouteMenu, TourismRouteDestiny, LodgingRoom, LodgingSchedule, LodgingType, LodgingService


class AgencyForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(AgencyForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True

    class Meta:
        model = Agency
        fields = '__all__'


class AgencyServiceForm(BaseForm):
    class Meta:
        model = AgencyService
        fields = '__all__'
        labels = {
            'agency': '',
        }
        widgets = {
            'agency': forms.HiddenInput(),
        }


class AgencyScheduleForm(BaseForm):
    class Meta:
        model = AgencySchedule
        fields = '__all__'
        labels = {
            'agency': '',
        }
        widgets = {
            'agency': forms.HiddenInput(),
        }


class EventForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True

    class Meta:
        model = Event
        fields = '__all__'


class LodgingForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(LodgingForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True

        self.fields["service"].widget = CheckboxSelectMultiple()
        self.fields["service"].queryset = LodgingService.objects.all()

    class Meta:
        model = Lodging
        fields = '__all__'


class LodgingRoomForm(BaseForm):
    class Meta:
        model = LodgingRoom
        fields = '__all__'
        labels = {
            'lodging': '',
        }
        widgets = {
            'lodging': forms.HiddenInput(),
        }


class LodgingScheduleForm(BaseForm):
    class Meta:
        model = LodgingSchedule
        fields = '__all__'
        labels = {
            'lodging': '',
        }
        widgets = {
            'lodging': forms.HiddenInput(),
        }


class LodgingTypeForm(BaseForm):
    class Meta:
        model = LodgingType
        fields = '__all__'


class LodgingServiceForm(BaseForm):
    class Meta:
        model = LodgingService
        fields = '__all__'


class RestaurantForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True

    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantMenuForm(BaseForm):
    class Meta:
        model = RestaurantMenu
        fields = '__all__'
        labels = {
            'restaurant': '',
        }
        widgets = {
            'restaurant': forms.HiddenInput(),
        }


class RestaurantScheduleForm(BaseForm):
    class Meta:
        model = RestaurantSchedule
        fields = '__all__'
        labels = {
            'restaurant': '',
        }
        widgets = {
            'restaurant': forms.HiddenInput(),
        }


class RestaurantServiceForm(BaseForm):
    class Meta:
        model = RestaurantService
        fields = '__all__'


class TourismRouteForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(TourismRouteForm, self).__init__(*args, **kwargs)
        self.fields['lat_origin'].widget.attrs['readonly'] = True
        self.fields['lng_origin'].widget.attrs['readonly'] = True
        self.fields['lat_destination'].widget.attrs['readonly'] = True
        self.fields['lng_destination'].widget.attrs['readonly'] = True

    class Meta:
        model = TourismRoute
        fields = '__all__'
        labels = {
            'destination': '',
        }
        widgets = {
            'destination': forms.HiddenInput(),
        }


class TourismRouteMenuForm(BaseForm):
    class Meta:
        model = TourismRouteMenu
        fields = '__all__'
        labels = {
            'route': '',
        }
        widgets = {
            'route': forms.HiddenInput(),
        }


class TourismRouteDestinyForm(BaseForm):
    class Meta:
        model = TourismRouteDestiny
        fields = '__all__'


class TourismSiteForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(TourismSiteForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True

    class Meta:
        model = TourismSite
        fields = '__all__'
        labels = {
            'destination': '',
        }
        widgets = {
            'destination': forms.HiddenInput(),
        }


class TourismSiteMenuForm(BaseForm):
    class Meta:
        model = TourismSiteMenu
        fields = '__all__'
        labels = {
            'site': '',
        }
        widgets = {
            'site': forms.HiddenInput(),
        }


class TourismSiteScheduleForm(BaseForm):
    class Meta:
        model = TourismSiteSchedule
        fields = '__all__'
        labels = {
            'site': '',
        }
        widgets = {
            'site': forms.HiddenInput(),
        }


class TourismSiteDestinyForm(BaseForm):
    class Meta:
        model = TourismSiteDestiny
        fields = '__all__'


class TourismSiteTypeForm(BaseForm):
    class Meta:
        model = TourismSiteType
        fields = '__all__'


class TourismSiteServiceForm(BaseForm):
    class Meta:
        model = TourismSiteService
        fields = '__all__'


class TransportForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(TransportForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True

    class Meta:
        model = Transport
        fields = '__all__'


class TransportDestinationForm(BaseForm):
    class Meta:
        model = TransportDestination
        fields = '__all__'
        labels = {
            'transport': '',
        }
        widgets = {
            'transport': forms.HiddenInput(),
        }

class TransportServiceForm(BaseForm):
    class Meta:
        model = TransportService
        fields = '__all__'


class TransportTypeServiceForm(BaseForm):
    class Meta:
        model = TransportTypeService
        fields = '__all__'
        labels = {
            'destination': '',
        }
        widgets = {
            'destination': forms.HiddenInput(),
        }


class TransportScheduleForm(BaseForm):
    class Meta:
        model = TransportSchedule
        fields = '__all__'
        labels = {
            'transport': '',
        }
        widgets = {
            'transport': forms.HiddenInput(),
        }