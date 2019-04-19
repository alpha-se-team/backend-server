from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Create your models here.


class UserProfile(models.Model):
    # uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # create_date = models.DateTimeField(auto_now_add=True)
    total_bandwidth = models.BigIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"UserProfile of {self.user.username}, total_bandwidth: {self.total_bandwidth}"
