# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0025_cancelarpedido_cancelarpedidows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancelarpedido',
            name='imagen',
            field=models.ImageField(upload_to=b'cancelarp/'),
        ),
        migrations.AlterField(
            model_name='cancelarpedidows',
            name='imagen',
            field=models.ImageField(upload_to=b'cancelarpw/'),
        ),
        migrations.AlterField(
            model_name='confirmarpedido',
            name='imagen',
            field=models.ImageField(upload_to=b'confirmarpedido/'),
        ),
        migrations.AlterField(
            model_name='confirmarpedidows',
            name='imagen',
            field=models.ImageField(upload_to=b'confirmarpedidows/'),
        ),
    ]
