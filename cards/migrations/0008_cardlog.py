# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cards', '0007_sharecardlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date published')),
                ('action', models.CharField(max_length=200, choices=[(b'added', b'added'), (b'removed', b'removed'), (b'updated', b'updated'), (b'created', b'created')])),
                ('card', models.ForeignKey(to='cards.Card')),
                ('cardlist', models.ForeignKey(to='cards.CardList')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
