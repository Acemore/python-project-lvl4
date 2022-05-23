from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import StatusForm
from .models import Status
from task_manager.mixins import CustomLoginRequiredMixin


STATUS_IN_USE = _('Невозможно удалить статус, потому что он используется')
SUCCESS_STATUS_CREATION = _('Статус успешно создан')
SUCCESS_STATUS_DELETING = _('Статус успешно удалён')
SUCCESS_STATUS_UPDATING = _('Статус успешно изменён')


class StatusCreationView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = SUCCESS_STATUS_CREATION


class StatusesListView(CustomLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusUpdatingView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = SUCCESS_STATUS_UPDATING


class StatusDeletingView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')
    success_message = SUCCESS_STATUS_DELETING

    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request, STATUS_IN_USE)
        else:
            messages.success(self.request, self.success_message)

        return redirect(self.success_url)
