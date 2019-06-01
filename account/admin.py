from django.contrib import admin
from .models import Account, Plan
# Register your models here.

admin.site.register(Account, Plan)
