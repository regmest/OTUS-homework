# Generated by Django 3.2.8 on 2021-11-07 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skillprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skilltag',
            name='slug',
            field=models.SlugField(default='slug', unique=True),
            preserve_default=False,
        ),
    ]