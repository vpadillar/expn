# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='empresa',
            field=models.ForeignKey(default=1, to='usuario.Empresa'),
            preserve_default=False,
        ),
    ]
