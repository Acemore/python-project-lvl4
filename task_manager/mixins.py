from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _


NOT_AUTHENTICATED_MESSAGE = (
    _('Вы не авторизованы! Пожалуйста, выполните вход.')
)


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, NOT_AUTHENTICATED_MESSAGE)
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)
