from tour_site.services import BaseForm
from .models import Event, Restaurant, Tourism_site, Transport, Lodgment, Agency


class EventForm(BaseForm):
    class Meta:
        model = Event
        fields = '__all__'


class RestaurantForm(BaseForm):
    class Meta:
        model = Restaurant
        fields = '__all__'


class TransportForm(BaseForm):
    class Meta:
        model = Transport
        fields = '__all__'


class Tourism_siteForm(BaseForm):
    class Meta:
        model = Tourism_site
        fields = '__all__'


class LodgmentForm(BaseForm):
    class Meta:
        model = Lodgment
        fields = '__all__'


class AgencyForm(BaseForm):
    class Meta:
        model = Agency
        fields = '__all__'

