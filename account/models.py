from django.db import models
from django.utils.translation import gettext_lazy as _


class Plan(models.Model):
    title = models.CharField(_('title'), max_length=128)
    description = models.TextField(_('description'), blank=True)
    total_bandwidth = models.BigIntegerField(_('total_bandwidth'), default=0)

    def __str__(self):
        return self.title


def get_sentinel_plan():
    return Plan.objects.get(title='_sentinel')[0]


class Profile(models.Model):
    user = models.OneToOneField(
        'authentication.User',
        on_delete=models.CASCADE,
        db_index=True,
    )
    active_plan = models.ForeignKey(Plan,
                                    on_delete=models.SET(get_sentinel_plan))
    amount_consumed = models.BigIntegerField(_('amount_consumed'))

    def __str__(self):
        return self.user.username
