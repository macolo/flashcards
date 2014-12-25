# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservalidationcode',
            name='hash',
            field=models.CharField(default=b'e737d9ae8c7711e4b1f0008865377db6', max_length=200, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
