from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.users.forms import CreateUserForm
from task_manager.users.models import User


NO_CHANGE_PERMISSION_MESSAGE = _(
    'У вас нет прав для изменения другого пользователя.',
)
SUCCESS_USER_CREATION = _('Пользователь успешно зарегистрирован')
SUCCESS_USER_DELETING = _('Пользователь успешно удалён')
SUCCESS_USER_UPDATING = _('Пользователь успешно изменён')
USER_IN_USE = _('Невозможно удалить пользователя, потому что он используется')


class UserListView(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'


class UserCreationView(SuccessMessageMixin, CreateView):
    # model = User
    form_class = CreateUserForm
    template_name = 'create_user.html'
    success_url = reverse_lazy('user_login')
    success_message = SUCCESS_USER_CREATION


class UserDeletingView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = User
    template_name = 'delete_user.html'
    success_url = reverse_lazy('users')
    success_message = SUCCESS_USER_DELETING

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object():
            messages.error(self.request, NO_CHANGE_PERMISSION_MESSAGE)
            return redirect('users')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, USER_IN_USE)
            return redirect(self.success_url)


class UserUpdatingView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = User
    form_class = CreateUserForm
    template_name = 'update_user.html'
    success_url = reverse_lazy('users')
    success_message = SUCCESS_USER_UPDATING

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object():
            messages.error(self.request, NO_CHANGE_PERMISSION_MESSAGE)
            return redirect('users')
        return super().get(request, *args, **kwargs)
