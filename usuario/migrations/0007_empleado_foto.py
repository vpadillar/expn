# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_ciudad_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='foto',
            field=models.ImageField(default=1, upload_to=b'empleado/'),
            preserve_default=False,
        ),
    ]
