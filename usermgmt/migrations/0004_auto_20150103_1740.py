# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0003_auto_20150103_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservalidationcode',
            name='hash',
            field=models.CharField(default=b'9fd54d72936f11e497c0f505d3c4f1d1', max_length=200, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
