from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.statuses.views import (
    SUCCESS_STATUS_CREATION, SUCCESS_STATUS_DELETING, SUCCESS_STATUS_UPDATING,
)
from task_manager.users.models import User


LOGIN_URL = '/login/'
NAME = 'name'
NEW_STATUS_NAME = 'status3'
STATUS_CREATION = 'create_status'
STATUS_DELETING = 'delete_status'
STATUS_UPDATING = 'update_status'
STATUSES = 'statuses'
STATUSES_LIST_URL = '/statuses/'
UPDATED_STATUS_NAME = 'status4'


# Create your tests here.
class TestStatuses(TestCase):
    fixtures = ["users.json", "statuses.json"]

    def setUp(self):
        self.user = User.objects.get(pk=1)

        self.first_status = Status.objects.get(pk=1)
        self.second_status = Status.objects.get(pk=2)

    def test_statuses_list(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse(STATUSES))

        self.assertEqual(resp.status_code, 200)

        statuses_list = list(resp.context[STATUSES])
        self.assertQuerysetEqual(
            statuses_list,
            [self.first_status, self.second_status]
        )

    def test_statuses_list_without_login(self):
        resp = self.client.get(reverse(STATUSES))
        self.assertRedirects(resp, LOGIN_URL)

    def test_status_creation(self):
        self.client.force_login(self.user)

        url = reverse(STATUS_CREATION)
        new_status = {
            NAME: NEW_STATUS_NAME,
        }
        resp = self.client.post(url, new_status, follow=True)

        self.assertRedirects(resp, STATUSES_LIST_URL)
        self.assertContains(resp, SUCCESS_STATUS_CREATION)

        created_status = Status.objects.get(name=new_status[NAME])
        self.assertEqual(created_status.name, NEW_STATUS_NAME)

    def test_status_updating(self):
        self.client.force_login(self.user)

        url = reverse(STATUS_UPDATING, args=(self.first_status.pk,))
        updated_status = {
            NAME: UPDATED_STATUS_NAME,
        }
        resp = self.client.post(url, updated_status, follow=True)

        self.assertRedirects(resp, STATUSES_LIST_URL)
        self.assertContains(resp, SUCCESS_STATUS_UPDATING)
        self.assertEqual(
            Status.objects.get(name=updated_status[NAME]),
            self.first_status
        )

    def test_status_deleting(self):
        self.client.force_login(self.user)

        url = reverse(STATUS_DELETING, args=(self.first_status.pk,))
        resp = self.client.post(url, follow=True)

        self.assertRedirects(resp, STATUSES_LIST_URL)
        self.assertContains(resp, SUCCESS_STATUS_DELETING)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=self.first_status.pk)
