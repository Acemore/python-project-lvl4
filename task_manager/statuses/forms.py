from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import Status


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = [
            'name',
        ]
        labels = {
            'name': _('Имя')
        }
