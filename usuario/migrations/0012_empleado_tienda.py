# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0011_auto_20160707_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='tienda',
            field=models.ForeignKey(default=3, to='usuario.Tienda'),
            preserve_default=False,
        ),
    ]
