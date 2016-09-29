from django import forms
from django.forms import widgets
from usuario import models as mod_usuario


class CiudadForm(forms.ModelForm):

    class Meta:
        model = mod_usuario.Opcion
        fields = ('ciudad',)
        widgets = {
            "ciudad": forms.Select(attrs={'class': 'ui search dropdown'}),
        }
    # end class
# end class
