from django.db import models
from django.utils.translation import gettext as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=100, null=False)

    description = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
    )

    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name=_('Исполнитель'),
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='status',
        verbose_name=_('Статус'),
    )

    labels = models.ManyToManyField(
        Label,
        related_name='labels',
        blank=True,
        through='TaskLabelRelation',
        through_fields=('task', 'label')
    )

    created_at = models.DateTimeField(auto_now_add=True)


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    label = models.ForeignKey(Label, on_delete=models.PROTECT)
