# -*- coding: utf-8 -*-
import re
from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.contrib.auth.hashers import make_password


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre
    # end def
# end class


class Usuario(User):
    TIPO_ID = (
        ("", "Tipo de identificación"),
        ('CEDULA', 'Cedula'),
        ('TARJETADEIDENTIDAD', 'Tarjeta de Identidad'),
        ('NIT', 'Nit'),
        ('PASAPORTE', 'Pasaporte')
    )

    tipo_id = models.CharField(max_length=20, choices=TIPO_ID)
    identificacion = models.CharField(max_length=15, unique=True, validators=[
                                      validators.RegexValidator(re.compile('^[0-9]+$'), ('identificacion no valida'), 'invalid')])
    telefono_fijo = models.CharField(max_length=15, blank=True, validators=[
                                     validators.RegexValidator(re.compile('^[0-9]+$'), ('telefono no valido'), 'invalid')])
    telefono_celular = models.CharField(max_length=15, validators=[validators.RegexValidator(
        re.compile('^[0-9]+$'), ('telefono no valido'), 'invalid')])


class Empresa(models.Model):
    first_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    nit = models.CharField(max_length=50, validators=[validators.RegexValidator(
        re.compile('^[0-9]+$'), ('numero no valida'))])
    logo = models.ImageField(upload_to='logos_empresas/')
    web = models.URLField()
    direccion = models.CharField(max_length=50)
    ciudad = models.ForeignKey(Ciudad)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
# end clas


class Tienda(models.Model):
    empresa = models.ForeignKey(Empresa)
    nit = models.CharField(max_length=50, unique=True)
    ciudad = models.ForeignKey(Ciudad)
    nombre = models.CharField(max_length=200)
    referencia = models.CharField(max_length=200)
    direccion = models.CharField(max_length=500)
    fijo = models.CharField(
        max_length=10, verbose_name="Telefono Fijo", null=True, blank=True)
    celular = models.CharField(
        max_length=10, verbose_name="Telefono Celular", null=True, blank=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    url = models.URLField()
    status = models.BooleanField(default=True)
    token = models.CharField(blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.nombre
    # end def
# end class


class Cliente (models.Model):
    TIPO_ID = (
        ("", "Tipo de identificación"),
        ('CEDULA', 'Cedula'),
        ('TARJETA DE IDENTIDAD', 'Tarjeta de Identidad'),
        ('NIT', 'Nit'),
        ('PASAPORTE', 'Pasaporte')
    )

    first_name = models.CharField(('Nombre'), max_length=50)
    last_name = models.CharField(('Apellido'), max_length=50)
    tipo_id = models.CharField(max_length=20, choices=TIPO_ID)
    identificacion = models.CharField(max_length=15, unique=True, validators=[
                                      validators.RegexValidator(re.compile('^[0-9]+$'), ('identificacion no valida'), 'invalid')])
    telefono_fijo = models.CharField(max_length=15, blank=True, validators=[
                                     validators.RegexValidator(re.compile('^[0-9]+$'), ('telefono no valido'), 'invalid')])
    telefono_celular = models.CharField(max_length=15, blank=True, validators=[
                                        validators.RegexValidator(re.compile('^[0-9]+$'), ('telefono no valido'), 'invalid')])
    direccion = models.CharField(max_length=50)
    barrio = models.CharField(max_length=50, blank=True)
    zona = models.CharField(max_length=50, blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad)
    empresa = models.ForeignKey(Empresa)

    def __str__(self):
        str = self.identificacion
        return str

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Empleado(Usuario):
    CARGOS = (
        ('', 'Selccion un Cargo'),
        ('ADMINISTRADOR', 'Administrador'),
        ('SUPERVISOR', 'Supervisor'),
        ('ALISTADOR', 'Alistador'),
        ('MOTORIZADO', 'Motorizado'),
    )
    fecha_nacimiento = models.DateField()
    cargo = models.CharField(max_length=20, choices=CARGOS)
    empresa = models.ForeignKey(Empresa)
    direccion = models.CharField(max_length=50)
    ciudad = models.ForeignKey(Ciudad)
    foto = models.ImageField(upload_to='empleado/', null=True, blank=True)
    tienda = models.ForeignKey(Tienda, null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def save(self, *args, **kwargs):
        if not len(self.password):
            self.password = make_password(self.identificacion)
        #
        super(Empleado, self).save(*args, **kwargs)
    # end def


class Opcion(models.Model):
    ciudad = models.ForeignKey(Ciudad)

    def __unicode__(self):
        return self.ciudad.nombre
    # end def

    def __str__(self):
        return self.ciudad.nombre
    # end def
# end class
