# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0013_opcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='tienda',
            field=models.ForeignKey(blank=True, to='usuario.Tienda', null=True),
        ),
    ]
