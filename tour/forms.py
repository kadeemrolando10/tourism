from django import forms
from django.forms import CheckboxSelectMultiple

from tour_site.services import BaseForm
from tour.models import Event, Restaurant, TourismSite, Transport, Lodging, Agency, TourismRoute, AgencyService, \
    AgencySchedule, RestaurantService, RestaurantSchedule, RestaurantMenu, TransportDestination, TransportService, \
    TransportTypeService, TransportSchedule, TourismSiteMenu, TourismSiteSchedule, TourismSiteDestiny, TourismSiteType, \
    TourismSiteService, TourismRouteMenu, TourismRouteDestiny, LodgingRoom, LodgingSchedule, LodgingType, \
    LodgingService, Client


class AgencyForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(AgencyForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True

    class Meta:
        model = Agency
        fields = '__all__'
        exclude = ['is_active']


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
        self.fields["event_date"].widget.attrs['class'] = 'datepicker'

    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['is_active']


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
        exclude = ['is_active']


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
        self.fields["service"].widget = CheckboxSelectMultiple()
        self.fields["service"].queryset = RestaurantService.objects.all()

    class Meta:
        model = Restaurant
        fields = '__all__'
        exclude = ['is_active']


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
        exclude = ['is_active']


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
        self.fields["service"].widget = CheckboxSelectMultiple()
        self.fields["service"].queryset = TourismSiteService.objects.all()

    class Meta:
        model = TourismSite
        fields = '__all__'
        exclude = ['is_active']


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
        exclude = ['is_active']


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
    def __init__(self, *args, **kwargs):
        super(TransportTypeServiceForm, self).__init__(*args, **kwargs)
        self.fields["service"].widget = CheckboxSelectMultiple()
        self.fields["service"].queryset = TransportService.objects.all()

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


class ClientForm(BaseForm):
    class Meta:
        model = Client
        exclude = ['user']

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name:
            if not first_name.replace(' ', '').isalpha():
                raise forms.ValidationError('Los Nombres no puede contener números')
            return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name:
            if not last_name.replace(' ', '').isalpha():
                raise forms.ValidationError('Los apellidos no puede contener números')
            return last_name


class ClientFormEdit(BaseForm):
    class Meta:
        model = Client
        exclude = ['user', 'rol']
