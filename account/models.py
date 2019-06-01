from django.db import models
from django.utils.translation import gettext_lazy as _


class Plan(models.Model):
    name = models.CharFiled(_('name'), max_length=128)
    totalBW = models.BigIntegerField(_('totalBW'))


class Account(models.Model):
    active_plan = models.OneToOneField(Plan, on_delete=models.PROTECT)
    consumed = models.BigIntegerField(_('consumed'))
