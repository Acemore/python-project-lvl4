from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label
from task_manager.mixins import CustomLoginRequiredMixin


LABEL_IN_USE = _('Невозможно удалить метку, потому что она используется')
LABELS = 'labels'
SUCCESS_LABEL_CREATION = _('Метка успешно создана')
SUCCESS_LABEL_DELETING = _('Метка успешно удалена')
SUCCESS_LABEL_UPDATING = _('Метка успешно изменена')


class LabelsListView(CustomLoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreationView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy(LABELS)
    success_message = SUCCESS_LABEL_CREATION


class LabelUpdatingView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy(LABELS)
    success_message = SUCCESS_LABEL_UPDATING


class LabelDeletingView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy(LABELS)
    success_message = SUCCESS_LABEL_DELETING

    def form_valid(self, form):
        try:
            self.get_object().delete()
        except ProtectedError:
            messages.error(self.request, LABEL_IN_USE)
        else:
            messages.success(self.request, self.success_message)

        return redirect(self.success_url)
