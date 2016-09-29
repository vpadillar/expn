# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0007_empleado_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='foto',
            field=models.ImageField(null=True, upload_to=b'empleado/', blank=True),
        ),
    ]
