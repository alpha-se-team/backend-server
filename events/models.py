from django.db import models

from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
# _ = lambda _: _


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
    title = models.CharField('title', max_length=128)
    text = models.TextField('content')
    img = models.ImageField(
        'img',
        # required=False,
        validators=[
            image_size_valid,
        ])  # 5 MiB limit

    def __str__(self):
        return f"""title: {self.title}
text: {self.text}"""
