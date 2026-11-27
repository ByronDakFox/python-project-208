from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

PASSWORD = 'Str0ng-pass-2026'


class TaskCrudTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='ana', password=PASSWORD,
            first_name='Ana', last_name='Pérez',
        )
        self.other = User.objects.create_user(
            username='luis', password=PASSWORD,
            first_name='Luis', last_name='Gómez',
        )
        self.status = Status.objects.create(name='nuevo')
        self.task = Task.objects.create(
            name='Primera', description='Texto',
            status=self.status, author=self.author,
        )

    def task_data(self, name):
        return {
            'name': name,
            'description': 'Descripción',
            'status': self.status.pk,
            'executor': self.other.pk,
        }

    def test_login_required(self):
        for url in (
            reverse('tasks_index'),
            reverse('tasks_create'),
            reverse('tasks_detail', args=[self.task.pk]),
            reverse('tasks_update', args=[self.task.pk]),
            reverse('tasks_delete', args=[self.task.pk]),
        ):
            self.assertRedirects(self.client.get(url), reverse('login'))

    def test_list_and_detail(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('tasks_index'))
        self.assertContains(response, 'Primera')
        response = self.client.get(
            reverse('tasks_detail', args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_create_sets_author(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse('tasks_create'), self.task_data('Segunda')
        )
        self.assertRedirects(response, reverse('tasks_index'))
        created = Task.objects.get(name='Segunda')
        self.assertEqual(created.author, self.other)

    def test_update(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse('tasks_update', args=[self.task.pk]),
            self.task_data('Renombrada'),
        )
        self.assertRedirects(response, reverse('tasks_index'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Renombrada')

    def test_delete_by_author(self):
        self.client.force_login(self.author)
        response = self.client.post(
            reverse('tasks_delete', args=[self.task.pk])
        )
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_by_other_user_denied(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse('tasks_delete', args=[self.task.pk])
        )
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_cannot_delete_user_with_tasks(self):
        self.client.force_login(self.author)
        self.client.post(reverse('users_delete', args=[self.author.pk]))
        self.assertTrue(User.objects.filter(pk=self.author.pk).exists())

    def test_cannot_delete_status_in_use(self):
        self.client.force_login(self.author)
        self.client.post(reverse('statuses_delete', args=[self.status.pk]))
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())


class TaskFilterTest(TestCase):
    def setUp(self):
        self.ana = User.objects.create_user(
            username='ana', password=PASSWORD,
        )
        self.luis = User.objects.create_user(
            username='luis', password=PASSWORD,
        )
        self.new = Status.objects.create(name='nuevo')
        self.done = Status.objects.create(name='terminado')
        self.bug = Label.objects.create(name='bug')

        self.t1 = Task.objects.create(
            name='T1', status=self.new, author=self.ana,
            executor=self.luis,
        )
        self.t2 = Task.objects.create(
            name='T2', status=self.done, author=self.luis,
        )
        self.t2.labels.add(self.bug)
        self.client.force_login(self.ana)

    def names(self, **params):
        response = self.client.get(reverse('tasks_index'), params)
        return {task.name for task in response.context['task_list']}

    def test_no_filter_shows_all(self):
        self.assertEqual(self.names(), {'T1', 'T2'})

    def test_filter_by_status(self):
        self.assertEqual(self.names(status=self.done.pk), {'T2'})

    def test_filter_by_executor(self):
        self.assertEqual(self.names(executor=self.luis.pk), {'T1'})

    def test_filter_by_label(self):
        self.assertEqual(self.names(label=self.bug.pk), {'T2'})

    def test_filter_self_tasks(self):
        self.assertEqual(self.names(self_tasks='on'), {'T1'})