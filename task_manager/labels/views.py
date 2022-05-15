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
    template_name = 'labels.html'
    context_object_name = 'labels'


class LabelCreationView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    # model = Label
    form_class = LabelForm
    template_name = 'create_label.html'
    success_url = reverse_lazy(LABELS)
    success_message = SUCCESS_LABEL_CREATION


class LabelUpdatingView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Label
    form_class = LabelForm
    template_name = 'update_label.html'
    success_url = reverse_lazy(LABELS)
    success_message = SUCCESS_LABEL_UPDATING


class LabelDeletingView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Label
    template_name = 'delete_label.html'
    success_url = reverse_lazy(LABELS)
    success_message = SUCCESS_LABEL_DELETING

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, LABEL_IN_USE)
            return redirect(self.success_url)
