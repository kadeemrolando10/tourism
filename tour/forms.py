from tour_site.services import BaseForm
from .models import Event


class EventForm(BaseForm):
    class Meta:
        model = Event
        fields = '__all__'

