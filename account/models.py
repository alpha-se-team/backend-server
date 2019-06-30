from django.db import models
from django.utils.translation import gettext_lazy as _


class Plan(models.Model):
    title = models.CharField(_('title'), max_length=128)
    description = models.TextField(_('description'), blank=True)
    total_bandwidth = models.BigIntegerField(_('total_bandwidth'), default=0)
    max_connected_devices = models.IntegerField(_('max_connected_devices'), default=2)

    def __str__(self):
        return self.title


def get_sentinel_plan():
    return Plan.objects.get(title='_sentinel')


class Profile(models.Model):
    user = models.OneToOneField(
        'authentication.User',
        on_delete=models.CASCADE,
        db_index=True,
    )
    active_plan = models.ForeignKey(Plan,
                                    on_delete=models.SET(get_sentinel_plan),
                                    default=get_sentinel_plan)

    connected_devices = models.IntegerField(_('connected_devices'), default=0)

    amount_consumed_down = models.BigIntegerField(_('amount_consumed_down'), default=0)
    amount_consumed_up = models.BigIntegerField(_('amount_consumed_up'), default=0)


    @classmethod
    def get_by_username(self, username):
        return self.objects.select_related('user').get(
            user__username=username)

    @property
    def amount_consumed(self):
        "Returns total amount of bandwith which is consumed."
        return self.amount_consumed_down + self.amount_consumed_up

    def add_device(self):
        if self.connected_devices <= self.active_plan.max_connected_devices:
            self.connected_devices += 1

    def remove_device(self):
        if 0 < self.connected_devices:
            self.connected_devices -= 1

    def remove_all_devices(self):
        self.connected_devices = 0

    def __str__(self):
        return self.user.username


class ProfileStats(models.Model):
    user = models.OneToOneField(
        'authentication.User',
        on_delete=models.CASCADE,
        db_index=True,
    )
    date = models.DateField(_('date'), auto_now_add=True)

    amount_consumed_down = models.BigIntegerField(_('amount_consumed_down'), default=0)
    amount_consumed_up = models.BigIntegerField(_('amount_consumed_up'), default=0)

    @classmethod
    def filter_by_username(self, queryset, username):
        return queryset.select_related('user').filter(user__username=username)

    def __str__(self):
        return f"{self.user.username}/{self.date} "
