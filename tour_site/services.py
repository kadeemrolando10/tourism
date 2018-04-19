import pytz
from datetime import datetime, timedelta
from django.forms.models import ModelForm
from django.forms.fields import BooleanField


class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-control border-input'


def convert_to_utc(string_date, is_end_date=False):
    local = pytz.timezone("America/La_Paz")
    date_new = datetime.strptime(string_date, "%Y-%m-%d")
    if is_end_date:
        date_new = date_new + timedelta(days=1)

    return local.localize(date_new, is_dst=None)


def convert_to_timezone(utc_dt):
    local_tz = pytz.timezone("America/La_Paz")
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)
