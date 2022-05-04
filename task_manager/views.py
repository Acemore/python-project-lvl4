from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


SUCCESS_LOGIN = _('Вы залогинены')
SUCCESS_LOGOUT = _('Вы разлогинены')


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('index')
    success_message = SUCCESS_LOGIN


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('index')
    logout_message = SUCCESS_LOGOUT

    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, self.logout_message)
        return super().dispatch(request, *args, **kwargs)
