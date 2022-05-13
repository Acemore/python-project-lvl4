from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import User
from .views import USER_IN_USE
from task_manager.tasks.models import Task


LOGIN_URL = '/login/'
SUCCESS_USER_CREATION = _('Пользователь успешно зарегистрирован')
SUCCESS_USER_DELETING = _('Пользователь успешно удалён')
SUCCESS_USER_UPDATING = _('Пользователь успешно изменён')
USER_CREATION = 'create_user'
USER_DELETING = 'delete_user'
USER_UPDATING = 'update_user'
USERNAME = 'username'
USERS = 'users'
USERS_LIST_URL = '/users/'


class TestUsers(TestCase):
    fixtures = ["users.json", "statuses.json", "tasks.json"]

    def setUp(self):
        self.first_user = User.objects.get(pk=1)
        self.second_user = User.objects.get(pk=2)

        # self.task = Task.objects.get(pk=1)

    def test_users_list(self):
        resp = self.client.get(reverse(USERS))
        users_list = list(resp.context[USERS])
        first_user, second_user = users_list

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(first_user.username, 'nick1')
        self.assertEqual(second_user.first_name, 'name2')

    def test_user_creation(self):
        url = reverse(USER_CREATION)
        new_user = {
            'first_name': 'name3',
            'last_name': 'surname3',
            'username': 'new_user',
            'password1': 'qpwoei102938',
            'password2': 'qpwoei102938',
        }
        resp = self.client.post(url, new_user, follow=True)

        self.assertRedirects(resp, LOGIN_URL)
        self.assertContains(resp, SUCCESS_USER_CREATION)

        created_user = User.objects.get(username=new_user[USERNAME])
        self.assertTrue(created_user.check_password('qpwoei102938'))

    def test_user_updating(self):
        user = self.first_user
        self.client.force_login(user)

        url = reverse(USER_UPDATING, args=[user.id, ])
        updated_user = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'password1': 'qpwoei1029389',
            'password2': 'qpwoei1029389',
        }
        resp = self.client.post(url, updated_user, follow=True)

        self.assertRedirects(resp, USERS_LIST_URL)
        self.assertContains(resp, SUCCESS_USER_UPDATING)

        changed_user = User.objects.get(username=user.username)
        self.assertTrue(changed_user.check_password('qpwoei1029389'))

    def test_user_deleting(self):
        self.client.force_login(self.first_user)
        Task.objects.all().delete()

        url = reverse(USER_DELETING, args=[self.first_user.id, ])
        resp = self.client.post(url, follow=True)

        self.assertRedirects(resp, USERS_LIST_URL)
        self.assertContains(resp, SUCCESS_USER_DELETING)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.first_user.id)

    def test_user_in_use_deleting(self):
        self.client.force_login(self.first_user)

        url = reverse(USER_DELETING, args=[self.first_user.pk, ])
        resp = self.client.post(url, follow=True)

        self.assertRedirects(resp, USERS_LIST_URL)
        self.assertContains(resp, USER_IN_USE)
        self.assertTrue(User.objects.filter(pk=self.first_user.pk).exists())
