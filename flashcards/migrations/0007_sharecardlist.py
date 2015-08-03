# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import flashcards.models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0006_auto_20141127_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareCardList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('secret', models.CharField(default=flashcards.models.generate_random_hash, unique=True, max_length=200)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date published')),
                ('cardlist', models.ForeignKey(to='flashcards.CardList')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
