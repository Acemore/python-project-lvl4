from django.test import TestCase
from django.urls import reverse

from .models import Label
from .views import (
    LABEL_IN_USE, SUCCESS_LABEL_CREATION,
    SUCCESS_LABEL_DELETING, SUCCESS_LABEL_UPDATING
)
from task_manager.tasks.models import Task
from task_manager.users.models import User


LABEL_CREATION = 'create_label'
LABEL_DELETING = 'delete_label'
LABEL_UPDATING = 'update_label'
LABELS = 'labels'
LABELS_LIST_URL = '/labels/'
LOGIN_URL = '/login/'
NAME = 'name'


class TestLabels(TestCase):
    fixtures = [
        "labels.json", "statuses.json", "task_label_rel.json",
        "tasks.json", "users.json"
    ]

    def setUp(self):
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)

        # self.task = Task.objects.get(pk=1)

        self.user = User.objects.get(pk=1)

    def test_labels_list(self):
        self.client.force_login(self.user)

        url = reverse(LABELS)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

        labels_list = list(resp.context[LABELS])
        self.assertQuerysetEqual(labels_list, [self.label1, self.label2])

    def test_labels_list_without_login(self):
        url = reverse(LABELS)
        resp = self.client.get(url)

        self.assertRedirects(resp, LOGIN_URL)

    def test_label_creation(self):
        self.client.force_login(self.user)

        url = reverse(LABEL_CREATION)
        new_label = {
            "name": "label3",
        }
        resp = self.client.post(url, new_label, follow=True)

        self.assertRedirects(resp, LABELS_LIST_URL)
        self.assertContains(resp, SUCCESS_LABEL_CREATION)

        created_label = Label.objects.get(name=new_label[NAME])
        self.assertEqual(created_label.name, "label3")

    def test_label_updating(self):
        self.client.force_login(self.user)

        url = reverse(LABEL_UPDATING, args=(self.label1.pk,))
        updated_label = {
            "name": "label4",
        }
        resp = self.client.post(url, updated_label, follow=True)

        self.assertRedirects(resp, LABELS_LIST_URL)
        self.assertContains(resp, SUCCESS_LABEL_UPDATING)
        self.assertEqual(
            Label.objects.get(name=updated_label[NAME]),
            self.label1
        )

    def test_label_deleting(self):
        self.client.force_login(self.user)
        Task.objects.all().delete()

        url = reverse(LABEL_DELETING, args=(self.label1.pk,))
        resp = self.client.post(url, follow=True)

        self.assertRedirects(resp, LABELS_LIST_URL)
        self.assertContains(resp, SUCCESS_LABEL_DELETING)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=self.label1.pk)

    def test_label_in_use_deleting(self):
        self.client.force_login(self.user)

        url = reverse(LABEL_DELETING, args=(self.label1.pk,))
        resp = self.client.post(url, follow=True)

        self.assertRedirects(resp, LABELS_LIST_URL)
        self.assertContains(resp, LABEL_IN_USE)
        self.assertTrue(Label.objects.filter(pk=1).exists())
