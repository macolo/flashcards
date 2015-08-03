# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0004_auto_20141127_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardlist',
            name='cards',
            field=models.ManyToManyField(related_name='cards', to='flashcards.Card', blank=True),
            preserve_default=True,
        ),
    ]
