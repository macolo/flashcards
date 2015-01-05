# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import usermgmt.models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0002_auto_20141225_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservalidationcode',
            name='hash',
            field=models.CharField(default=usermgmt.models.generate_random_hash, unique=True, max_length=200, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
