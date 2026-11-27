from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.users.forms import UserForm


class UserPermissionMixin(UserPassesTestMixin):
    """Solo el propio usuario puede editar o eliminar su cuenta."""

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.pk == self.kwargs['pk']

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'No has iniciado sesión. Por favor, inicia sesión.',
            )
            return redirect('login')
        messages.error(
            self.request,
            'No tienes permiso para modificar a otro usuario.',
        )
        return redirect('users_index')


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    success_message = 'Usuario registrado con éxito'
    extra_context = {'title': 'Registro', 'button_text': 'Registrar'}


class UserUpdateView(
    UserPermissionMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('users_index')
    success_message = 'Usuario actualizado con éxito'
    extra_context = {
        'title': 'Cambiar usuario',
        'button_text': 'Editar',
    }


class UserDeleteView(
    UserPermissionMixin, SuccessMessageMixin, DeleteView
):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')
    success_message = 'Usuario eliminado con éxito'

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                'No se puede eliminar el usuario porque está en uso.',
            )
            return redirect('users_index')