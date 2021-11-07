from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=False)
    about = models.TextField(null=True, blank=True)
