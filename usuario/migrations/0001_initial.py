# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.contrib.auth.models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50, verbose_name=b'Nombre')),
                ('last_name', models.CharField(max_length=50, verbose_name=b'Apellido')),
                ('tipo_id', models.CharField(max_length=20, choices=[(b'', b'Tipo de identificaci\xc3\xb3n'), (b'CEDULA', b'Cedula'), (b'TARJETA DE IDENTIDAD', b'Tarjeta de Identidad'), (b'NIT', b'Nit'), (b'PASAPORTE', b'Pasaporte')])),
                ('identificacion', models.CharField(unique=True, max_length=15, validators=[django.core.validators.RegexValidator(re.compile(b'^[0-9]+$'), b'identificacion no valida', b'invalid')])),
                ('telefono_fijo', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(re.compile(b'^[0-9]+$'), b'telefono no valido', b'invalid')])),
                ('telefono_celular', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(re.compile(b'^[0-9]+$'), b'telefono no valido', b'invalid')])),
                ('direccion', models.CharField(max_length=50)),
                ('barrio', models.CharField(max_length=50, blank=True)),
                ('zona', models.CharField(max_length=50, null=True, blank=True)),
                ('ciudad', models.ForeignKey(to='usuario.Ciudad')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('nit', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(re.compile(b'^[0-9]+$'), b'numero no valida')])),
                ('logo', models.ImageField(upload_to=b'logos_empresas/')),
                ('web', models.URLField()),
                ('direccion', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('ciudad', models.ForeignKey(to='usuario.Ciudad')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nit', models.CharField(unique=True, max_length=50)),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=500)),
                ('fijo', models.CharField(max_length=10, null=True, verbose_name=b'Telefono Fijo', blank=True)),
                ('celular', models.CharField(max_length=10, null=True, verbose_name=b'Telefono Celular', blank=True)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('empresa', models.ForeignKey(to='usuario.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tipo_id', models.CharField(max_length=20, choices=[(b'', b'Tipo de identificaci\xc3\xb3n'), (b'CEDULA', b'Cedula'), (b'TARJETADEIDENTIDAD', b'Tarjeta de Identidad'), (b'NIT', b'Nit'), (b'PASAPORTE', b'Pasaporte')])),
                ('identificacion', models.CharField(unique=True, max_length=15, validators=[django.core.validators.RegexValidator(re.compile(b'^[0-9]+$'), b'identificacion no valida', b'invalid')])),
                ('telefono_fijo', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(re.compile(b'^[0-9]+$'), b'telefono no valido', b'invalid')])),
                ('telefono_celular', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(re.compile(b'^[0-9]+$'), b'telefono no valido', b'invalid')])),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('usuario_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='usuario.Usuario')),
                ('fecha_nacimiento', models.DateField()),
                ('cargo', models.CharField(max_length=20, choices=[(b'', b'Selccion un Cargo'), (b'ADMINISTRADOR', b'Administrador'), (b'SUPERVISOR', b'Supervisor'), (b'ALISTADOR', b'Alistador'), (b'MOTORIZADO', b'Motorizado')])),
                ('direccion', models.CharField(max_length=50)),
                ('ciudad', models.ForeignKey(to='usuario.Ciudad')),
                ('empresa', models.ForeignKey(to='usuario.Empresa')),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
            },
            bases=('usuario.usuario',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
