from django import forms

from tour_site.services import BaseForm
from .models import Event, Restaurant, TourismSite, Transport, Lodging, Agency


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'title',
            'image',
            'service',
            'menu',
            'schedule',
            'address',
            'location',
            'phone',
            'rating',
            'web'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'service': forms.CheckboxSelectMultiple(attrs={'class': 'form-controll'}),
            'menu': forms.CheckboxSelectMultiple(attrs={'class': 'form-controll'}),
            'schedule': forms.CheckboxSelectMultiple(attrs={'class': 'form-controll'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.URLInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.TextInput(attrs={'class': 'form-control'}),
            'web': forms.TextInput(attrs={'class': 'form-control'})
        }


class EventForm(BaseForm):
    class Meta:
        model = Event
        fields = '__all__'


class TransportForm(BaseForm):
    class Meta:
        model = Transport
        fields = '__all__'


class TourismSiteForm(BaseForm):
    class Meta:
        model = TourismSite
        fields = '__all__'


class LodgingForm(BaseForm):
    class Meta:
        model = Lodging
        fields = '__all__'


class AgencyForm(BaseForm):
    class Meta:
        model = Agency
        fields = '__all__'
