# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_auto_20141127_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='cardlist',
        ),
        migrations.RemoveField(
            model_name='cardlist',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='cardlist',
            name='users',
        ),
        migrations.AddField(
            model_name='cardlist',
            name='cards',
            field=models.ManyToManyField(to='cards.Card'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cardlistgroup',
            name='mode',
            field=models.CharField(default=b'r', max_length=4, choices=[(b'r', b'read'), (b'cr', b'create and read'), (b'crud', b'create, read, update and delete')]),
            preserve_default=True,
        ),
    ]
