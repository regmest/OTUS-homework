import string
import random
from slugify import slugify as py_slugify

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


def random_slug(length: int):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


class SkillTag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    class Meta:
        unique_together = (("author_user", "name"),)

    STATUS_CHOICES = [
        ("not started", "Not started"),
        ("in progress", "In progress"),
        ("postponed", "Postponed"),
        ("finished", "Finished"),
        ("failed", "Failed")
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    author_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=256, blank=False, null=False)
    status = models.CharField(null=False, blank=False, max_length=64, choices=STATUS_CHOICES,
                              default=STATUS_CHOICES[0][0])
    description = models.TextField(null=True, blank=True)
    tag = models.ManyToManyField(SkillTag, blank=True, null=True)
    slug = models.SlugField(null=False, unique=True)

    # progress_percent = models.PositiveSmallIntegerField(null=True, blank=True)  # на будущее, когда будет добавлен расчет

    def __str__(self):
        return self.name

    def tags(self):
        return ", ".join([d.name for d in self.tag.all()])

    def get_general_details_url(self):
        return reverse('skill-detail', kwargs={'slug': self.slug})

    def get_userskill_details_url(self):
        return reverse('user-skill-detail', kwargs={'slug': self.slug, 'username': self.author_user.username})

    def save(self, *args, **kwargs):
        self.slug = py_slugify(self.name) + "-" + random_slug(3)
        super(Skill, self).save(*args, **kwargs)