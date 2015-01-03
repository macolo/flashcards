# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0002_auto_20141225_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservalidationcode',
            name='hash',
            field=models.CharField(default=b'0a6b14ba936f11e497c081e02033cb8f', max_length=200, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
