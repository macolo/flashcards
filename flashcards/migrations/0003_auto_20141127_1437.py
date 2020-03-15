# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flashcards', '0002_auto_20141116_0020'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardListGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mode', models.CharField(default=b'r', max_length=4, choices=[(b'r', b'Read'), (b'cr', b'Read, Create'), (b'crud', b'Full')])),
                ('cardlist', models.ForeignKey(to='flashcards.CardList', on_delete=models.PROTECT)),
                ('groups', models.ForeignKey(to='auth.Group', on_delete=models.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardListUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mode', models.CharField(default=b'r', max_length=4, choices=[(b'r', b'Read'), (b'cr', b'Read, Create'), (b'crud', b'Full')])),
                ('cardlist', models.ForeignKey(to='flashcards.CardList', on_delete=models.PROTECT)),
                ('users', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='card',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cardlist',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cardlist',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cardlist',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
