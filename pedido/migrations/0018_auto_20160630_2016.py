# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0017_confirmarpedido_confirmarpedidows'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='confirmarpedido',
            options={'verbose_name': 'Confirmacion Pedido', 'verbose_name_plural': 'Confirmaciones Pedidos'},
        ),
        migrations.AlterModelOptions(
            name='confirmarpedidows',
            options={'verbose_name': 'Confirmacion PedidoWS', 'verbose_name_plural': 'Confirmaciones PedidoWS'},
        ),
        migrations.RemoveField(
            model_name='confirmarpedido',
            name='motorizado',
        ),
        migrations.RemoveField(
            model_name='confirmarpedidows',
            name='motorizado',
        ),
    ]
