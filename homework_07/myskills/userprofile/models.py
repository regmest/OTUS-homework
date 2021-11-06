from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User


class UserInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=False)
    about = models.TextField(null=True, blank=True)


class SkillTag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)
    description = models.TextField(null=True, blank=True)

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
    author_user = models.ForeignKey(User, on_delete=models.PROTECT,
                                    null=True)  # TODO автор должен заполняться автоматически
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

    def get_user_details_url(self):
        return reverse('user-skill-detail', kwargs={'slug': self.slug, 'username': self.author_user.username})

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(str(self.name) + "-" + str(self.author_user))
    #     return super().save(*args, **kwargs)
