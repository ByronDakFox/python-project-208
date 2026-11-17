from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

PASSWORD = 'Str0ng-pass-2026'


class UserCrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ana', password=PASSWORD,
            first_name='Ana', last_name='Pérez',
        )
        self.other = User.objects.create_user(
            username='luis', password=PASSWORD,
            first_name='Luis', last_name='Gómez',
        )

    def form_data(self, username):
        return {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': username,
            'password1': PASSWORD,
            'password2': PASSWORD,
        }

    def test_list_is_public(self):
        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(
            reverse('users_create'), self.form_data('nuevo')
        )
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='nuevo').exists())

    def test_update(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_update', args=[self.user.pk]),
            self.form_data('ana2'),
        )
        self.assertRedirects(response, reverse('users_index'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'ana2')

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_delete', args=[self.user.pk])
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_cannot_update_other_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_update', args=[self.other.pk]),
            self.form_data('hackeado'),
        )
        self.assertRedirects(response, reverse('users_index'))
        self.other.refresh_from_db()
        self.assertEqual(self.other.username, 'luis')

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(
            reverse('users_update', args=[self.user.pk])
        )
        self.assertRedirects(response, reverse('login'))