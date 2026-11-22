from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from task_manager.mixins import AuthRequiredMixin
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskAuthorMixin(UserPassesTestMixin):
    """Solo el autor de la tarea puede eliminarla."""

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Una tarea solo puede ser eliminada por su autor.',
        )
        return redirect('tasks_index')


class TaskListView(AuthRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'

    def get_queryset(self):
        return Task.objects.select_related('status', 'author', 'executor')


class TaskDetailView(AuthRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'La tarea se creó correctamente.'
    extra_context = {'title': 'Crear tarea', 'button_text': 'Crear'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'La tarea se modificó correctamente.'
    extra_context = {'title': 'Cambiar tarea', 'button_text': 'Cambiar'}


class TaskDeleteView(
    AuthRequiredMixin, TaskAuthorMixin, SuccessMessageMixin, DeleteView
):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'La tarea se eliminó correctamente.'