from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class AuthRequiredMixin(LoginRequiredMixin):
    """Solo usuarios con sesión iniciada."""

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(
            self.request,
            'No has iniciado sesión. Por favor, inicia sesión.',
        )
        return redirect('login')