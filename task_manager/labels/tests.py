from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class LabelCrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ana', password='Str0ng-pass-2026',
        )
        self.label = Label.objects.create(name='bug')

    def test_login_required(self):
        for url in (
            reverse('labels_index'),
            reverse('labels_create'),
            reverse('labels_update', args=[self.label.pk]),
            reverse('labels_delete', args=[self.label.pk]),
        ):
            self.assertRedirects(self.client.get(url), reverse('login'))

    def test_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('labels_index'))
        self.assertContains(response, 'bug')

    def test_create(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('labels_create'), {'name': 'urgente'}
        )
        self.assertRedirects(response, reverse('labels_index'))
        self.assertTrue(Label.objects.filter(name='urgente').exists())

    def test_update(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('labels_update', args=[self.label.pk]),
            {'name': 'mejora'},
        )
        self.assertRedirects(response, reverse('labels_index'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'mejora')

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('labels_delete', args=[self.label.pk])
        )
        self.assertRedirects(response, reverse('labels_index'))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_cannot_delete_label_in_use(self):
        status = Status.objects.create(name='nuevo')
        task = Task.objects.create(
            name='Tarea', status=status, author=self.user,
        )
        task.labels.add(self.label)
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('labels_delete', args=[self.label.pk])
        )
        self.assertRedirects(response, reverse('labels_index'))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())