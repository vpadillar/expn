from django.contrib import admin
import models

# Register your models here.
admin.site.register(models.Items)
admin.site.register(models.Pedido)
admin.site.register(models.ConfirmarPedido)
admin.site.register(models.ConfirmarPedidoWs)
admin.site.register(models.CancelarPedido)
admin.site.register(models.CancelarPedidoWs)
admin.site.register(models.ItemsPedido)
admin.site.register(models.PedidoWS)
admin.site.register(models.ConfiguracionTiempo)
