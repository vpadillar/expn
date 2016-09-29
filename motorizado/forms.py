# -*- coding: utf-8 -*-

from django import forms
from django.forms import widgets
from models import *
from usuario.models import Empleado, Empresa
from django.db.models import Q


class AddTecnoForm(forms.ModelForm):

    class Meta:
        model = Tecno
        fields = '__all__'
        widgets = {
            "numeroT": forms.TextInput(attrs={'placeholder': 'Numero'}),
            "fecha_expedicionT": forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder': 'Fecha de Expedición', 'type': 'date'}),
            "fecha_expiracionT": forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder': 'Fecha de Expiracion', 'type': 'date'}),
        }

    def clean_fecha_expiracionT(self):
        dictionay_clean = self.cleaned_data

        fecha_expedicionT = dictionay_clean.get('fecha_expedicionT')
        fecha_expiracionT = dictionay_clean.get('fecha_expiracionT')

        if fecha_expedicionT >= fecha_expiracionT:
            raise forms.ValidationError(
                "La fecha de Expiracion debe ser mayor que la de expedicion")

        return fecha_expiracionT


class AddSoatForm(forms.ModelForm):

    class Meta:
        model = Soat
        fields = '__all__'
        widgets = {
            "numeroS": forms.TextInput(attrs={'placeholder': 'Numero'}),
            "fecha_expedicionS": forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder': 'Fecha de Expedición', 'type': 'date'}),
            "fecha_expiracionS": forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder': 'Fecha de Expiracion', 'type': 'date'}),
        }

    def clean_fecha_expiracionS(self):
        dictionay_clean = self.cleaned_data

        fecha_expedicionS = dictionay_clean.get('fecha_expedicionS')
        fecha_expiracionS = dictionay_clean.get('fecha_expiracionS')

        if fecha_expedicionS >= fecha_expiracionS:
            raise forms.ValidationError(
                "La fecha de Expiracion debe ser mayor que la de expedicion")

        return fecha_expiracionS


class AddMotoForm(forms.ModelForm):

    class Meta:
        model = Moto
        fields = '__all__'
        exclude = ('soat', 'tecno',)
        widgets = {
            "marca": forms.TextInput(attrs={'placeholder': 'Marca'}),
            "tipo": forms.TextInput(attrs={'placeholder': 'Tipo'}),
            "placa": forms.TextInput(attrs={'placeholder': 'Placa'}),
            "t_propiedad": forms.TextInput(attrs={'placeholder': 'Tarjeta de Propiedad'}),
            "empresaM": forms.Select(attrs={'class': 'ui search dropdown'}),
        }


class AddMotoApiForm(forms.ModelForm):

    class Meta:
        model = Moto
        fields = '__all__'
        exclude = ('soat', 'tecno', 'empresaM',)
        widgets = {
            "marca": forms.TextInput(attrs={'placeholder': 'Marca'}),
            "tipo": forms.TextInput(attrs={'placeholder': 'Tipo'}),
            "placa": forms.TextInput(attrs={'placeholder': 'Placa'}),
            "t_propiedad": forms.TextInput(attrs={'placeholder': 'Tarjeta de Propiedad'}),
        }


class AddMotorizadoForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(queryset=Empleado.objects.filter(
        cargo='MOTORIZADO', motorizado__empleado__isnull=True), widget=forms.Select(attrs={'class': 'ui fluid search selection dropdown'}))

    class Meta:
        model = Motorizado
        fields = '__all__'
        exclude = ('moto',)
        widgets = {
            "licencia": forms.TextInput(attrs={'placeholder': 'Licencia'}),
            "identifier": forms.TextInput(attrs={'placeholder': 'Identificador'}),
        }


class editMotorizadoForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(queryset=Empleado.objects.filter(
        cargo='MOTORIZADO'), widget=forms.Select(attrs={'class': 'ui fluid search selection dropdown'}))

    def __init__(self, *args, **kwargs):
        super(editMotorizadoForm, self).__init__(*args, **kwargs)
        q = Q(motorizado__moto__isnull=True, estado=True)
        if self.instance.moto:
            q = q | Q(pk=self.instance.moto.pk)
        # end if
        moto = forms.ModelChoiceField(queryset=Moto.objects.filter(
            q), widget=forms.Select(attrs={'class': 'ui fluid search selection dropdown'}))
    # end def

    class Meta:
        model = Motorizado
        fields = '__all__'
        widgets = {
            "licencia": forms.TextInput(attrs={'placeholder': 'Licencia'}),
            "identifier": forms.TextInput(attrs={'placeholder': 'Identificador'}),
            "moto": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "empleado": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
        }


class AddMotorizadoApiForm(forms.ModelForm):

    class Meta:
        model = Motorizado
        fields = '__all__'
        exclude = ('moto',)
        widgets = {
            "licencia": forms.TextInput(attrs={'placeholder': 'Licencia'}),
            "identifier": forms.TextInput(attrs={'placeholder': 'Identificador'}),
            "empleado": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
        }


class AsignarMotoForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(queryset=Empleado.objects.filter(
        cargo='MOTORIZADO', motorizado__empleado__isnull=True), widget=forms.Select(attrs={'class': 'ui fluid search selection dropdown'}))
    moto = forms.ModelChoiceField(queryset=Moto.objects.filter(motorizado__moto__isnull=True,
                                                               estado=True), widget=forms.Select(attrs={'class': 'ui fluid search selection dropdown'}))

    class Meta:
        model = Motorizado
        fields = '__all__'
        widgets = {
            "licencia": forms.TextInput(attrs={'placeholder': 'Licencia'}),
            "identifier": forms.TextInput(attrs={'placeholder': 'Identificador'}),
        }


class AsignarMotoApiForm(forms.ModelForm):

    class Meta:
        model = Motorizado
        exclude = ('identifier',)
        widgets = {
            "licencia": forms.TextInput(attrs={'placeholder': 'Licencia'}),
            "empleado": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "moto": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
        }

class AsignarMotoForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(queryset=Empleado.objects.filter(
        cargo='MOTORIZADO', motorizado__empleado__isnull=True), widget=forms.Select(attrs={'class': 'ui fluid search selection dropdown'}))
    moto = forms.ModelChoiceField(queryset=Moto.objects.filter(motorizado__moto__isnull=True,
                                                               estado=True), widget=forms.Select(attrs={'class': 'ui fluid search selection dropdown'}))

    class Meta:
        model = Motorizado
        fields = '__all__'
        widgets = {
            "licencia": forms.TextInput(attrs={'placeholder': 'Licencia'}),
            "identifier": forms.TextInput(attrs={'placeholder': 'Identificador'}),
        }


class reporteForm(forms.Form):
    ciudad = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'ui fluid search selection dropdown', 'required': ''}), required=True)
    fecha_inicio = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'placeholder': 'Fecha de Inicio', 'required': '', 'type': 'date'}))
    fecha_final = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'placeholder': 'Fecha Final', 'required': '', 'type': 'date'}))
# enc class
