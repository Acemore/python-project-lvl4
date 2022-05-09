from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import User


class TestUsers(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.first_user = User.objects.get(pk=1)
        self.second_user = User.objects.get(pk=2)

    def test_users_list(self):
        resp = self.client.get(reverse('users'))
        users_list = list(resp.context['users'])
        first_user, second_user = users_list

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(first_user.username, 'nick1')
        self.assertEqual(second_user.first_name, 'name2')

    def test_user_creation(self):
        url = reverse('create_user')
        new_user = {
            'first_name': 'name3',
            'last_name': 'surname3',
            'username': 'new_user',
            'password1': 'qpwoei102938',
            'password2': 'qpwoei102938',
        }
        resp = self.client.post(url, new_user, follow=True)

        self.assertRedirects(resp, '/login/')

        self.assertContains(resp, 'Пользователь успешно зарегистрирован')

        created_user = User.objects.get(username=new_user['username'])
        self.assertTrue(created_user.check_password('qpwoei102938'))

    def test_user_updating(self):
        user = self.first_user
        self.client.force_login(user)

        url = reverse('update_user', args=[user.id, ])
        updated_user = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'password1': 'qpwoei1029389',
            'password2': 'qpwoei1029389',
        }
        resp = self.client.post(url, updated_user, follow=True)

        self.assertRedirects(resp, '/users/')

        self.assertContains(resp, 'Пользователь успешно изменён')

        changed_user = User.objects.get(username=user.username)
        self.assertTrue(changed_user.check_password('qpwoei1029389'))

    def test_user_deleting(self):
        self.client.force_login(self.first_user)

        url = reverse('delete_user', args=[self.first_user.id, ])
        resp = self.client.post(url, follow=True)

        self.assertRedirects(resp, '/users/')

        self.assertContains(resp, 'Пользователь успешно удалён')

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.first_user.id)
