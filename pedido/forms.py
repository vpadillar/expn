# -*- coding: utf-8 -*-
from django import forms
import models
from usuario import models as usuario
from django.core.exceptions import ValidationError


class AddPedidoApiForm(forms.ModelForm):

    class Meta:
        model = models.Pedido
        fields = '__all__'
        exclude = ('motorizado', 'total', 'supervisor',
                   'empresa', 'npedido_express',)
        widgets = {
            "num_pedido": forms.TextInput(attrs={'placeholder': 'Numero de Pedido'}),
            "tienda": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "cliente": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "alistador": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "tipo_pago": forms.Select(attrs={'class': 'ui dropdown'}),
            "observacion": forms.Textarea(attrs={'rows': '4', 'placeholder': 'Observaciones'}),
        }


class AddPedidoAdminApiForm(forms.ModelForm):

    class Meta:
        model = models.Pedido
        fields = '__all__'
        exclude = ('total', 'empresa', 'npedido_express', 'motorizado',)
        widgets = {
            "num_pedido": forms.TextInput(attrs={'placeholder': 'Numero de Pedido'}),
            "tienda": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "cliente": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "tipo_pago": forms.Select(attrs={'class': 'ui dropdown'}),
            "observacion": forms.Textarea(attrs={'rows': '4', 'placeholder': 'Observaciones'}),
            "alistador": forms.Select(attrs={'class': 'ui fluid search selection dropdown', 'required': 'true'}),
            "supervisor": forms.Select(attrs={'class': 'ui fluid search selection dropdown', 'required': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        empresa = kwargs.pop('num_pedido', 0)
        pedido = models.Pedido.objects.filter(empresa__id=empresa)
        if pedido:
            pedido = pedido.latest('id')
            nom_pedido = '%s_%d' % (pedido.empresa.first_name[0:2].upper(), int(
                pedido.num_pedido.split('_')[1]) + 1)
        elif empresa > 0:
            emp = usuario.Empresa.objects.filter(id=empresa).first()
            nom_pedido = '%s_%d' % (emp.first_name[0:2].upper(), 1)
        else:
            nom_pedido = 'Ex_1'
        # end if
        kwargs.update(initial={
            # 'field': 'value'
            'num_pedido': nom_pedido
        })
        super(AddPedidoAdminApiForm, self).__init__(*args, **kwargs)


class AddItemsApiForm(forms.ModelForm):

    class Meta:
        model = models.Items
        fields = '__all__'
        exclude = ('empresaI',)
        widgets = {
            "codigo": forms.TextInput(attrs={'placeholder': 'Codigo'}),
            "descripcion": forms.Textarea(attrs={'rows': '2', 'placeholder': 'Descripción'}),
            "presentacion": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
        }


class AddItemsForm(forms.ModelForm):

    class Meta:
        model = models.Items
        fields = '__all__'
        widgets = {
            "codigo": forms.TextInput(attrs={'placeholder': 'Codigo'}),
            "descripcion": forms.Textarea(attrs={'rows': '2', 'placeholder': 'Descripción'}),
            "presentacion": forms.Select(attrs={'class': 'ui fluid search selection dropdown', 'placeholder': 'Presentacion'}),
            "empresaI": forms.Select(attrs={'class': 'ui fluid search selection dropdown', 'placeholder': 'Empresa'}),
        }


class AddItemsPedidoForm(forms.ModelForm):

    class Meta:
        model = models.ItemsPedido
        fields = '__all__'
        exclude = ('pedido', 'valor_total',)
        widgets = {
            "cantidad": forms.NumberInput(attrs={'placeholder': 'Cantidad'}),
            "valor_unitario": forms.NumberInput(attrs={'placeholder': 'Valor Unitario'}),
            "item": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
        }

        def clean(self):
            print self
            clean_data = super(AddItemsPedidoForm, self).clean()
            cantidad = clean_data.get("cantidad")
            valor_unitario = clean_data.get("valor_unitario")
            if cantidad < 0:
                self.add_error('cantidad', 'Numero debe ser mayor a 0')
            # end if
            if valor_unitario < 0:
                self.add_error('valor_unitario', 'valor_unitario debe ser mayor a 0')
            # end if
        # end def

class EditPedidoAdminApiForm(forms.ModelForm):

    class Meta:
        model = models.Pedido
        fields = '__all__'
        exclude = ('total', 'empresa', 'npedido_express',)
        widgets = {
            "num_pedido": forms.TextInput(attrs={'placeholder': 'Numero de Pedido'}),
            "tienda": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "cliente": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "tipo_pago": forms.Select(attrs={'class': 'ui dropdown'}),
            "observacion": forms.Textarea(attrs={'rows': '4', 'placeholder': 'Observaciones'}),
            "alistador": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "supervisor": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
            "motorizado": forms.Select(attrs={'class': 'ui fluid search selection dropdown'}),
        }
    # end class

    def __init__(self, *args, **kwargs):
        super(EditPedidoAdminApiForm, self).__init__(*args, **kwargs)
    # end def
# end class


class AddConfiguracion(forms.ModelForm):
    class Meta:
        model = models.ConfiguracionTiempo
        fields = ('retraso', 'pedido', 'distancia',
                  'gps', 'primero', 'segundo', 'empresa',)
        exclude = ('empresa',)
        widgets = {
            'retraso': forms.NumberInput(attrs={'placeholder': 'Tiempo retraso del motorizado(Min)'}),
            'pedido': forms.NumberInput(attrs={'placeholder': 'Tiempo de retraso del pedido(Min)'}),
            'distancia': forms.NumberInput(attrs={'placeholder': 'Distancia para asignacion de pedido(Mts)'}),
            'gps': forms.NumberInput(attrs={'placeholder': 'Tiempo de envío de Gps(Min)'}),
            'primero': forms.NumberInput(attrs={'placeholder': 'Primer corte de quincena'}),
            'segundo': forms.NumberInput(attrs={'placeholder': 'Segundo corte de quincena'}),
        }
    # end class

    def clean(self):
        print self
        clean_data = super(AddConfiguracion, self).clean()
        primero = clean_data.get("primero")
        segundo = clean_data.get("segundo")
        if primero > 31:
            self.add_error('primero', 'Numero debe ser menor a 31')
        # end if
        if segundo > 31:
            self.add_error('segundo', 'Numero debe ser menor a 31')
        # end if
        if primero > segundo:
            self.add_error('primero', 'Numero debe ser menor a el segundo valor')
        # end if
    # end def

# end class
