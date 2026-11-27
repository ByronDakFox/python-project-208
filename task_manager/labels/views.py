from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.mixins import AuthRequiredMixin


class LabelListView(AuthRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'


class LabelCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/form.html'
    success_url = reverse_lazy('labels_index')
    success_message = 'Etiqueta creada con éxito'
    extra_context = {'title': 'Crear etiqueta', 'button_text': 'Crear'}


class LabelUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/form.html'
    success_url = reverse_lazy('labels_index')
    success_message = 'Etiqueta modificada con éxito'
    extra_context = {'title': 'Cambiar etiqueta', 'button_text': 'Editar'}


class LabelDeleteView(AuthRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_index')
    success_message = 'Etiqueta eliminada con éxito'

    def form_valid(self, form):
        if self.object.tasks.exists():
            messages.error(
                self.request,
                'No se puede eliminar la etiqueta porque está en uso.',
            )
            return redirect('labels_index')
        return super().form_valid(form)