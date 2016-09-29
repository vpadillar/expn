# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0027_auto_20160717_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEnvio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('empresa', models.CharField(max_length=1000)),
                ('status', models.CharField(max_length=1000)),
                ('response', models.CharField(max_length=10000)),
            ],
        ),
    ]
