# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_sharecardlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_answer',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_question',
            field=models.CharField(max_length=600),
        ),
    ]
