from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .forms import TaskFilter, TaskForm
from .models import Task
from task_manager.mixins import CustomLoginRequiredMixin


NO_DELETE_PERMISSION_MESSAGE = _('Задачу может удалить только её автор')
SUCCESS_TASK_CREATION = _('Задача успешно создана')
SUCCESS_TASK_DELETING = _('Задача успешно удалена')
SUCCESS_TASK_UPDATING = _('Задача успешно изменена')
TASK_DETAILS = 'task_details'
TASKS = 'tasks'


class TasksListView(CustomLoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks.html'
    context_object_name = TASKS
    filterset_class = TaskFilter


class TaskDetailsView(CustomLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = TASK_DETAILS


class TaskCreationView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    # model = Task
    form_class = TaskForm
    template_name = 'create_task.html'
    success_url = reverse_lazy(TASKS)
    success_message = SUCCESS_TASK_CREATION

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdatingView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Task
    form_class = TaskForm
    template_name = 'update_task.html'
    success_url = reverse_lazy(TASKS)
    success_message = SUCCESS_TASK_UPDATING


class TaskDeletingView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Task
    template_name = 'delete_task.html'
    success_url = reverse_lazy(TASKS)
    success_message = SUCCESS_TASK_DELETING

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            messages.error(self.request, NO_DELETE_PERMISSION_MESSAGE)
            return redirect(TASKS)
        return super().get(request, *args, **kwargs)
