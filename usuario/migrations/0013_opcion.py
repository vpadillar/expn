# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0012_empleado_tienda'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opcion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ciudad', models.ForeignKey(to='usuario.Ciudad')),
            ],
        ),
    ]
