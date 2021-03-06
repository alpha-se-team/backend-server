import jwt

from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
# _ = lambda _: _



def image_size_valid(val):
    def file_size(value, limitKB):
        limitKB *= 1024
        if value.size > limitKB:
            raise ValidationError(
                f'File too large. Size should not exceed {limitKB} KiB.')

    file_size(val, 5 * 1024)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    # `db_index` is `True` for attrs which are common for retrive queries
    username = models.CharField(
        _('username'),
        db_index=True,
        max_length=255,
        unique=True,
        help_text=
        _('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
         ),
        validators=[username_validator],
        error_messages={
            _('unique'): _("A user with that username already exists."),
        },
    )

    student_id = models.CharField(_('student_id') ,max_length=128, blank=True)
    first_name = models.CharField(_('first_name'), max_length=128, blank=True)
    last_name = models.CharField(_('last_name'), max_length=128, blank=True)

    img = models.BinaryField(
        _('img'),
        null=True,
        # required=False,
        validators=[
            image_size_valid,
        ])  # 5 MiB limit

    email = models.EmailField(_('email address'),
                              blank=True,
                              db_index=True,
                              unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_as'), auto_now=True)

    last_connection_at = models.DateTimeField(_('last_connection_at'),
                                              auto_now=True)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # Tells Djanog that the UserManager class should manage objects of this type
    objects = UserManager()

    def __str__(self):
        return f"{self.username}: {self.email}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm=settings.JWT_AUTH['JWT_ALGORITHM'])

        return token.decode('utf-8')
