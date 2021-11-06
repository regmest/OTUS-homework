from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Direction(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    nickname = models.CharField(max_length=32, blank=False, null=False, unique=True)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nickname


class UserSkillProfile(models.Model):

    STATUS_CHOICES = [
        ("not started", "Not started"),
        ("in progress", "In progress"),
        ("postponed", "Postponed"),
        ("finished", "Finished"),
        ("failed", "Failed")
    ]

    user = models.ForeignKey(UserInfo, on_delete=models.PROTECT, blank=False, null=False)
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT, blank=False, null=False)
    direction = models.ManyToManyField(Direction)
    parent_skill = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True)
    status = models.CharField(null=False, blank=False, max_length=64, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    progress_percent = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.skill.name

    def get_directions(self):
        return ", ".join([d.name for d in self.direction.all()])






