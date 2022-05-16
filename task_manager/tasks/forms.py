from django.forms import CheckboxInput, ModelForm
from django.utils.translation import gettext as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from .models import Task
from task_manager.labels.models import Label


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'labels',
        ]
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
            'executor': _('Исполнитель'),
            'labels': _('Метки'),
        }


class TaskFilter(FilterSet):
    labels = ModelChoiceFilter(
        label=_('Метка'),
        queryset=Label.objects.all(),
    )
    own_tasks = BooleanFilter(
        label=_('Только свои задачи'),
        method='filter_own_tasks',
        widget=CheckboxInput,
    )

    def filter_own_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = [
            'status',
            'executor',
        ]
