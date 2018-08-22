from django import forms
from django.forms import CheckboxSelectMultiple

from tour_site.services import BaseForm
from tour.models import Event, Restaurant, TourismSite, Transport, Lodging, Agency, TourismRoute, AgencyService, \
    AgencySchedule, RestaurantService, RestaurantSchedule, RestaurantMenu, TransportDestination, TransportService, \
    TransportTypeService, TransportSchedule, TourismSiteMenu, TourismSiteSchedule, Location, TourismSiteType, \
    TourismSiteService, TourismRouteMenu, LodgingRoom, LodgingSchedule, LodgingType, \
    LodgingService, Client, Objective, Function, Secretary, Law, Social

from django.core.validators import URLValidator


class SocialForm(BaseForm):
    facebook = forms.URLField(validators=[URLValidator()])
    instagram = forms.URLField(validators=[URLValidator()])
    youtube = forms.URLField(validators=[URLValidator()])
    twitter = forms.URLField(validators=[URLValidator()])
    whatsapp = forms.URLField(validators=[URLValidator()])

    def __init__(self, *args, **kwargs):
        super(SocialForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True

    class Meta:
        model = Social
        fields = '__all__'


class AgencyForm(BaseForm):
    web = forms.URLField(validators=[URLValidator()])

    def __init__(self, *args, **kwargs):
        super(AgencyForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True
        self.fields["image"].widget.attrs['class'] = 'inputfile'
        self.fields["phone"].widget.attrs['data-inputmask'] = "'mask':[ '+(999) 999-99999']"
        self.fields["phone"].widget.attrs['data-mask'] = True

    class Meta:
        model = Agency
        fields = '__all__'
        exclude = ['is_active']


class AgencyServiceForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(AgencyServiceForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs['class'] = 'inputfile'

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
        self.fields["event_date"].widget.attrs['class'] = 'date pull-right datepicker'
        self.fields["file"].widget.attrs['class'] = 'inputfile'

    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['is_active']


class LodgingForm(BaseForm):
    web = forms.URLField(validators=[URLValidator()])

    def __init__(self, *args, **kwargs):
        super(LodgingForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True
        self.fields["service"].widget = CheckboxSelectMultiple()
        self.fields["service"].queryset = LodgingService.objects.all()
        self.fields["image"].widget.attrs['class'] = 'inputfile'
        self.fields["phone"].widget.attrs['data-inputmask'] = "'mask':[ '+(999) 999-99999']"
        self.fields["phone"].widget.attrs['data-mask'] = True

    class Meta:
        model = Lodging
        fields = '__all__'
        exclude = ['is_active']


class LodgingRoomForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(LodgingRoomForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs['class'] = 'inputfile'

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
    def __init__(self, *args, **kwargs):
        super(LodgingScheduleForm, self).__init__(*args, **kwargs)
        self.fields["schedule"].widget.attrs['data-inputmask'] = "'mask':[ 'h:s - h:s']"
        self.fields["schedule"].widget.attrs['data-mask'] = True

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
    def __init__(self, *args, **kwargs):
        super(LodgingServiceForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs['class'] = 'inputfile'

    class Meta:
        model = LodgingService
        fields = '__all__'


class RestaurantForm(BaseForm):
    web = forms.URLField(validators=[URLValidator()])

    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True
        self.fields["service"].widget = CheckboxSelectMultiple()
        self.fields["service"].queryset = RestaurantService.objects.all()
        self.fields["image"].widget.attrs['class'] = 'inputfile'
        self.fields["phone"].widget.attrs['data-inputmask'] = "'mask':[ '+(999) 999-99999']"
        self.fields["phone"].widget.attrs['data-mask'] = True

    class Meta:
        model = Restaurant
        fields = '__all__'
        exclude = ['is_active']


class RestaurantMenuForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(RestaurantMenuForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs['class'] = 'inputfile'

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
    def __init__(self, *args, **kwargs):
        super(RestaurantServiceForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs['class'] = 'inputfile'

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
        self.fields["date"].widget.attrs['class'] = 'date pull-right datepicker'
        self.fields["image"].widget.attrs['class'] = 'inputfile'

    class Meta:
        model = TourismRoute
        fields = '__all__'
        exclude = ['is_active']


class TourismRouteMenuForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(TourismSiteMenuForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs['class'] = 'inputfile'

    class Meta:
        model = TourismRouteMenu
        fields = '__all__'
        labels = {
            'route': '',
        }
        widgets = {
            'route': forms.HiddenInput(),
        }


class LocationForm(BaseForm):
    class Meta:
        model = Location
        fields = '__all__'


class TourismSiteForm(BaseForm):
    web = forms.URLField(validators=[URLValidator()])

    def __init__(self, *args, **kwargs):
        super(TourismSiteForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True
        self.fields["service"].widget = CheckboxSelectMultiple()
        self.fields["service"].queryset = TourismSiteService.objects.all()
        self.fields["image"].widget.attrs['class'] = 'inputfile'
        self.fields["phone"].widget.attrs['data-inputmask'] = "'mask':[ '+(999) 999-99999']"
        self.fields["phone"].widget.attrs['data-mask'] = True

    class Meta:
        model = TourismSite
        fields = '__all__'
        exclude = ['is_active']


class TourismSiteMenuForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(TourismSiteMenuForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs['class'] = 'inputfile'

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


class TourismSiteTypeForm(BaseForm):
    class Meta:
        model = TourismSiteType
        fields = '__all__'


class TourismSiteServiceForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(TourismSiteServiceForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs['class'] = 'inputfile'

    class Meta:
        model = TourismSiteService
        fields = '__all__'


class TransportForm(BaseForm):
    web = forms.URLField(validators=[URLValidator()])

    def __init__(self, *args, **kwargs):
        super(TransportForm, self).__init__(*args, **kwargs)
        self.fields['lat'].widget.attrs['readonly'] = True
        self.fields['lng'].widget.attrs['readonly'] = True
        self.fields["image"].widget.attrs['class'] = 'inputfile'
        self.fields["phone"].widget.attrs['data-inputmask'] = "'mask':[ '+(999) 999-99999']"
        self.fields["phone"].widget.attrs['data-mask'] = True

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
    def __init__(self, *args, **kwargs):
        super(TransportServiceForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs['class'] = 'inputfile'

    class Meta:
        model = TransportService
        fields = '__all__'


class TransportTypeServiceForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(TransportTypeServiceForm, self).__init__(*args, **kwargs)
        self.fields["service"].widget = CheckboxSelectMultiple()
        self.fields["service"].queryset = TransportService.objects.all()
        self.fields["image_bus"].widget.attrs['class'] = 'inputfile'
        self.fields["image_seat"].widget.attrs['class'] = 'inputfile'

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


class ObjectiveForm(BaseForm):
    class Meta:
        model = Objective
        fields = '__all__'


class FunctionForm(BaseForm):
    class Meta:
        model = Function
        fields = '__all__'
        exclude = ['is_active']


class SecretaryForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(SecretaryForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs['class'] = 'inputfile'

    class Meta:
        model = Secretary
        fields = '__all__'


class LawForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(LawForm, self).__init__(*args, **kwargs)
        self.fields["file"].widget.attrs['class'] = 'class="inputfile'

    class Meta:
        model = Law
        fields = '__all__'
        exclude = ['is_active']