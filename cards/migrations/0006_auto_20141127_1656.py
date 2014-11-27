# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cards', '0005_auto_20141127_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardlist',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', through='cards.CardListGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardlist',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='cards.CardListUser'),
            preserve_default=True,
        ),
    ]
