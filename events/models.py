from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def file_size(value, limitKB):
    limitKB *= 1024
    if value.size > limitKB:
        raise ValidationError(
            f'File too large. Size should not exceed {limitKB} KiB.')


def image_size_valid(val):
    file_size(val, 5 * 1024)


class TimestampedMixin(models.Model):
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_as'), auto_now=True)

    class Meta:
        abstract = True


class Event(TimestampedMixin, models.Model):
    title = models.CharField(_('title'), max_length=128)
    text = models.TextField(_('text'))
    due = models.DateTimeField(_('due'), default=timezone.datetime.now)
    img = models.BinaryField(
        _('img'),
        null=True,
        # required=False,
        validators=[
            image_size_valid,
        ])  # 5 MiB limit

    def __str__(self):
        return f"title: {self.title}, text: {self.text}"
