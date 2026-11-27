from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status


class StatusCrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ana', password='Str0ng-pass-2026',
        )
        self.status = Status.objects.create(name='nuevo')

    def test_login_required(self):
        urls = [
            reverse('statuses_index'),
            reverse('statuses_create'),
            reverse('statuses_update', args=[self.status.pk]),
            reverse('statuses_delete', args=[self.status.pk]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, reverse('login'))

    def test_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'nuevo')

    def test_create(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('statuses_create'), {'name': 'en progreso'}
        )
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertTrue(Status.objects.filter(name='en progreso').exists())

    def test_update(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('statuses_update', args=[self.status.pk]),
            {'name': 'terminado'},
        )
        self.assertRedirects(response, reverse('statuses_index'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'terminado')

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('statuses_delete', args=[self.status.pk])
        )
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())