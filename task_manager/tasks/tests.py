from django.test import TestCase
from django.urls import reverse

from .models import Task
from .views import (
    NO_DELETE_PERMISSION_MESSAGE, SUCCESS_TASK_CREATION,
    SUCCESS_TASK_DELETING, SUCCESS_TASK_UPDATING
)
# from task_manager.statuses.models import Status
from task_manager.users.models import User


LOGIN_URL = '/login/'
NAME = 'name'
TASK_CREATION = 'create_task'
TASK_DELETING = 'delete_task'
TASK_UPDATING = 'update_task'
TASKS = 'tasks'
TASKS_LIST_URL = '/tasks/'


class TestTasks(TestCase):
    fixtures = [
        "labels.json", "statuses.json", "task_label_rel.json",
        "tasks.json", "users.json"
    ]

    def setUp(self):
        # self.status1 = Status.objects.get(pk=1)
        # self.status2 = Status.objects.get(pk=2)

        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

        self.task = {
            "name": "task3",
            "description": "text3",
            "author": 1,
            "executor": 2,
            "status": 1
        }

    def test_tasks_list(self):
        self.client.force_login(self.user1)
        resp = self.client.get(reverse(TASKS))

        self.assertEqual(resp.status_code, 200)

        tasks_list = list(resp.context[TASKS])
        self.assertQuerysetEqual(tasks_list, [self.task1, self.task2])

    def test_tasks_list_without_login(self):
        resp = self.client.get(reverse(TASKS))
        self.assertRedirects(resp, LOGIN_URL)

    def test_task_creation(self):
        self.client.force_login(self.user1)
        resp = self.client.post(reverse(TASK_CREATION), self.task, follow=True)

        self.assertRedirects(resp, TASKS_LIST_URL)
        self.assertContains(resp, SUCCESS_TASK_CREATION)

        created_task = Task.objects.get(name=self.task[NAME])
        self.assertEqual(created_task.name, "task3")

    def test_task_updating(self):
        self.client.force_login(self.user1)

        url = reverse(TASK_UPDATING, args=(self.task1.pk,))
        updated_task = {
            "name": "updated_name",
            "description": "updated_text",
            "author": 1,
            "executor": 2,
            "status": 1,
        }
        resp = self.client.post(url, updated_task, follow=True)

        self.assertRedirects(resp, TASKS_LIST_URL)
        self.assertContains(resp, SUCCESS_TASK_UPDATING)
        self.assertEqual(Task.objects.get(name=updated_task[NAME]), self.task1)

    def test_task_deleting(self):
        self.client.force_login(self.user1)

        url = reverse(TASK_DELETING, args=(self.task1.pk,))
        resp = self.client.post(url, follow=True)

        self.assertRedirects(resp, TASKS_LIST_URL)
        self.assertContains(resp, SUCCESS_TASK_DELETING)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task1.pk)

    def test_task_deleting_by_not_author(self):
        self.client.force_login(self.user2)

        url = reverse(TASK_DELETING, args=(self.task1.pk,))
        resp = self.client.get(url, follow=True)

        self.assertRedirects(resp, TASKS_LIST_URL)
        self.assertContains(resp, NO_DELETE_PERMISSION_MESSAGE)
        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())

    def test_filter_by_status(self):
        self.client.force_login(self.user1)

        filtered_list = f"{reverse(TASKS)}?status=1"
        resp = self.client.get(filtered_list)

        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(list(resp.context[TASKS]), [self.task1])

    def test_filter_by_executor(self):
        self.client.force_login(self.user1)

        filtered_list = f"{reverse(TASKS)}?executor=1"
        resp = self.client.get(filtered_list)

        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(list(resp.context[TASKS]), [self.task2])

    def test_filter_by_label(self):
        self.client.force_login(self.user1)

        filtered_list = f"{reverse(TASKS)}?labels=1"
        resp = self.client.get(filtered_list)

        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(
            list(resp.context[TASKS]),
            [self.task1, self.task2]
        )

    def test_filter_own_tasks(self):
        self.client.force_login(self.user1)

        filtered_list = f"{reverse(TASKS)}?own_tasks=on"
        resp = self.client.get(filtered_list)

        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(list(resp.context[TASKS]), [self.task1])
