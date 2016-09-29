# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cedulaC', models.ImageField(upload_to=b'cedulas/')),
                ('clienteC', models.ForeignKey(to='usuario.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(unique=True, max_length=50)),
                ('descripcion', models.TextField(max_length=150)),
                ('presentacion', models.CharField(default=b'UNIDAD', max_length=50, choices=[(b'UNIDAD', b'Unidad'), (b'GRAMO', b'Gramo'), (b'LITRO', b'Litros')])),
                ('status', models.BooleanField(default=True)),
                ('empresaI', models.ForeignKey(to='usuario.Empresa')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='ItemsPedido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.DecimalField(max_digits=20, decimal_places=2)),
                ('valor_unitario', models.DecimalField(max_digits=20, decimal_places=2)),
                ('valor_total', models.DecimalField(max_digits=20, decimal_places=2)),
                ('item', models.ForeignKey(to='pedido.Items')),
            ],
            options={
                'verbose_name': 'Item Pedido',
                'verbose_name_plural': 'Items Pedido',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_pedido', models.CharField(max_length=50)),
                ('npedido_express', models.CharField(unique=True, max_length=50)),
                ('fecha_pedido', models.DateField(auto_now=True)),
                ('tienda', models.CharField(max_length=50, null=True, blank=True)),
                ('tipo_pago', models.CharField(default=b'EFECTIVO', max_length=50, choices=[(b'EFECTIVO', b'Efectivo'), (b'TARJETA', b'Tarjeta'), (b'REMISION', b'Remision')])),
                ('observacion', models.TextField(max_length=200, null=True, blank=True)),
                ('total', models.DecimalField(null=True, max_digits=20, decimal_places=2)),
                ('entregado', models.BooleanField(default=False)),
                ('despachado', models.BooleanField(default=False)),
                ('confirmado', models.BooleanField(default=False)),
                ('alistado', models.BooleanField(default=False)),
                ('alistador', models.ForeignKey(related_name='alistador', to='usuario.Empleado')),
                ('cliente', models.ForeignKey(to='usuario.Cliente', null=True)),
                ('empresa', models.ForeignKey(to='usuario.Empresa')),
                ('motorizado', models.ForeignKey(related_name='motorizado_enviado', to='usuario.Empleado', null=True)),
                ('supervisor', models.ForeignKey(related_name='supervisor', to='usuario.Empleado')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='PedidoWS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_pedido', models.CharField(max_length=50)),
                ('npedido_express', models.CharField(max_length=50)),
                ('fecha_pedido', models.DateField(auto_now=True)),
                ('tienda', models.CharField(max_length=50, null=True, blank=True)),
                ('cliente', models.CharField(max_length=300, null=True, blank=True)),
                ('tipo_pago', models.CharField(max_length=50)),
                ('observacion', models.TextField(max_length=200, null=True, blank=True)),
                ('total', models.DecimalField(null=True, max_digits=20, decimal_places=2)),
                ('entregado', models.BooleanField(default=False)),
                ('despachado', models.BooleanField(default=False)),
                ('confirmado', models.BooleanField(default=False)),
                ('alistado', models.BooleanField(default=False)),
                ('items', models.CharField(max_length=2000, null=True, blank=True)),
                ('alistador', models.ForeignKey(related_name='alistadorws', to='usuario.Empleado', null=True)),
                ('empresa', models.ForeignKey(blank=True, to='usuario.Empresa', null=True)),
                ('motorizado', models.ForeignKey(related_name='motorizado_enviadows', to='usuario.Empleado', null=True)),
                ('supervisor', models.ForeignKey(related_name='supervisorws', to='usuario.Empleado', null=True)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='Tiempo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tiempo_pedido', models.DateTimeField()),
                ('tiempo_asignacion', models.DateTimeField(null=True)),
                ('tiempo_entrego', models.DateTimeField(null=True)),
                ('pedido', models.OneToOneField(to='pedido.Pedido')),
            ],
            options={
                'verbose_name': 'Tiempo',
                'verbose_name_plural': 'Tiempos',
            },
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creado', models.DateTimeField()),
                ('confirmado', models.DateTimeField(null=True)),
                ('alistado', models.DateTimeField(null=True)),
                ('despachado', models.DateTimeField(null=True)),
                ('entregado', models.DateTimeField(null=True)),
                ('pedido', models.OneToOneField(to='pedido.Pedido')),
            ],
            options={
                'verbose_name': 'Time',
                'verbose_name_plural': 'Times',
            },
        ),
        migrations.CreateModel(
            name='TimeWS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creado', models.DateTimeField()),
                ('confirmado', models.DateTimeField(null=True)),
                ('alistado', models.DateTimeField(null=True)),
                ('despachado', models.DateTimeField(null=True)),
                ('entregado', models.DateTimeField(null=True)),
                ('pedido', models.OneToOneField(to='pedido.PedidoWS')),
            ],
        ),
        migrations.AddField(
            model_name='itemspedido',
            name='pedido',
            field=models.ForeignKey(to='pedido.Pedido'),
        ),
        migrations.AddField(
            model_name='certificado',
            name='pedidoC',
            field=models.ForeignKey(to='pedido.Pedido'),
        ),
    ]
