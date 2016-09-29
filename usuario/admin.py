from django.contrib import admin
import models
import forms


class CiudadAdmin(admin.ModelAdmin):
    pass
# end class


class EmpresaAdmin(admin.ModelAdmin):
    pass
# end class


class TiendaAdmin(admin.ModelAdmin):
    pass
# end class


class ClienteAdmin(admin.ModelAdmin):
    pass
# end class


"""
class EmpleadoAdmin(admin.ModelAdmin):
    form = forms.AddEmpleadoApiForm
# end class
"""
# Administracion de Empleado


class EmpleadoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Informacion Personal', {'fields': ['username', 'first_name', 'last_name',
                                             'tipo_id', 'identificacion', 'cargo', 'fecha_nacimiento', 'empresa', 'is_active']}),
        ('Informacion de Contacto', {'fields': [
         'telefono_fijo', 'telefono_celular', 'email', 'direccion', 'ciudad','foto']}),
    ]
    list_display = ('first_name', 'last_name', 'cargo', 'empresa',)


admin.site.register(models.Ciudad, CiudadAdmin)
admin.site.register(models.Empresa, EmpresaAdmin)
admin.site.register(models.Tienda, TiendaAdmin)
admin.site.register(models.Cliente, ClienteAdmin)
admin.site.register(models.Empleado, EmpleadoAdmin)
