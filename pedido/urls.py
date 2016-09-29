from django.conf.urls import patterns, url
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


# Gestion de pedido
urlpatterns = [
    url(r'^pedido/$', login_required(TemplateView.as_view(template_name='pedido/index.html')), name='index_pedido'),
    url(r'^pedido/admin/add/$', login_required(views.AddPedidoAdmin.as_view()), name='add_admin_pedido'),
    url(r'^pedido/edit/(?P<pk>\d+)/$', login_required(views.EditPedido.as_view()), name='edit_pedido'),
    url(r'^pedido/info/(?P<pk>\d+)/$', login_required(views.InfoPedido.as_view()), name='info_pedido'),
    url(r'^pedido/factura/(?P<pk>\d+)/$', login_required(views.FacturaPedido.as_view(template_name='pedido/factura.html')), name='factura_pedido'),
    url(r'^pedido/list/$', login_required(TemplateView.as_view(template_name='pedido/pedidosSearch.html')), name='list_pedido'),
    url(r'^pedido/search/$', login_required(views.TablaPedido.as_view()), name='search_pedido'),
    url(r'^pedido/mis/$', login_required(views.MisPedidos.as_view()), name='mis_pedido'),
    url(r'^pedido/mis/pedidos/$', login_required(views.TablaMisPedidos.as_view()), name='pedidos_pedido'),
]

# Gestion de despacho
urlpatterns += [
    url(r'^despacho/$', login_required(views.Despacho.as_view()), name='despachar_pedido'),
    url(r'^pedido/despacho/search/$', login_required(views.TablaDespachoPedido.as_view()), name='despachar_search_pedido'),
    url(r'^pedido/despacho/update/$', login_required(views.UpdateServicePedido.as_view()), name='despachar_update_pedido'),
    url(r'^pedido/entrega/update/$', login_required(views.UpdateEntregaServicePedido.as_view()), name='entrega_update_pedido'),
]

# Gestion de Item
urlpatterns += [
    url(r'^pedido/add/item/(?P<pk>\d+)/$', login_required(views.AddItemPedido.as_view()), name='add_item_pedido'),
    url(r'^pedido/finalizar/(?P<pk>\d+)/$', login_required(views.FinalizarPedido.as_view()), name='final_item_pedido'),
    url(r'^item/add/$', login_required(views.AddItem.as_view()), name='add_item'),
    url(r'^item/edit/(?P<pk>\d+)/$', login_required(views.UpdateItem.as_view()), name='edit_item'),
    url(r'^item/list/$', login_required(TemplateView.as_view(template_name='pedido/itemsSearch.html')), name='list_item'),
    url(r'^item/search/$', login_required(views.TablaItems.as_view()), name='search_item'),
    url(r'^item/delete/(?P<pk>\d+)/(?P<id_pedido>\d+)/$', login_required(views.DeleteItemPedido.as_view()), name='delete_item_pedido'),
]

# Gestion Asignacion Motorizado a Pedido
urlpatterns += [
    url(r'^asignar/motorizado/$', login_required(views.AsignarMotorizado.as_view()), name='asignar_motorizado_pedido'),
    url(r'^asignar/motorizado/search/$', login_required(views.TablaPedidosAsignar.as_view()), name='tabla_asignar_motorizado_pedido'),
    url(r'^asignar/motorizado/pedido/(?P<pedido_id>\d+)/$', login_required(views.AsignarPedidoMotorizado.as_view()), name='motorizado_asignar_pedido'),
    url(r'^asignar/motorizado/close/(?P<pedido_id>\d+)/$', login_required(views.CAMotorizado.as_view()), name='motorizado_cerrar_asignar_pedido'),

]

# Getsion de actualizacion de pedidos
urlpatterns += [
    url(r'^motorizado/up/ser/pedido/$', login_required(views.UpSerPedido.as_view()), name='mot_up_serPedido'),
    url(r'^motorizado/up/ser/entrega/$', login_required(views.UpdPedSerEntrega.as_view()), name='up_ser_entrega_pedido'),
]


# Getsion de actualizacion de pedidos
urlpatterns += [
    url(r'^emp/ws/pedido/$', views.WsPedidoEmpresa.as_view(), name='ws_serPedido'),
]


# Gestion de Ws
urlpatterns += [
    url(r'^rastreo/$', login_required(views.Rastreo.as_view()), name='rastreo'),
    url(r'^res/ws/pedido/$', login_required(views.UpSerPedido.as_view()), name='up_serPedido'),
]


# Gestion de recepcion de pedido
urlpatterns += [
    url(r'^aceptar/pws/$', views.AceptarPWService.as_view(), name='aceptar_pwservice'),
    url(r'^aceptar/pplataforma/$', views.AceptarPPlataforma.as_view(), name='aceptar_pplataforma'),
]


# Gestion de recoger de pedido
urlpatterns += [
    url(r'^recoger/pplataforma/$', views.RecogerPPlataforma.as_view(), name='recoger_pplataforma'),
    url(r'^recoger/pws/$', views.RecogerPWService.as_view(), name='recoger_wservice'),
]


# Gestion de entrega de pedido
urlpatterns += [
    url(r'^entregar/pplataforma/$', views.EntregarPPlataforma.as_view(), name='entregar_pplataforma'),
    url(r'^entregar/pws/$', views.EntregarPWService.as_view(), name='entregar_wservice'),
]


# Gestion de entrega de pedido
urlpatterns += [
    url(r'^confirmar/pplataforma/$', views.ConfirmacionPedido.as_view(), name='confirmar_pplataforma'),
    url(r'^confirmar/pws/$', views.ConfirmacionPedidoWS.as_view(), name='confirmar_wservice'),
]


# Gestion de cancelar de pedido
urlpatterns += [
    url(r'^cancelar/pplataforma/$', views.CancelarPPlataforma.as_view(), name='cancelar_pplataforma'),
    url(r'^cancelar/pws/$', views.CancelarPWService.as_view(), name='cancelar_wservice'),
]


# Gestion de reactivar de pedido
urlpatterns += [
    url(r'^reactivar/pplataforma/$', views.ReactivarPPlataforma.as_view(), name='reactivar_pplataforma'),
]


# Gestion de Configuracion de tiempos
urlpatterns += [
    url(r'^configuracion/$', views.ConfiguracionTiempo.as_view(), name='configurar_pplataforma'),
]


# Gestion Auto Asignar Pedido
urlpatterns += [
    url(r'^autoasignar/$', views.AutoAsignar.as_view(), name='autoasignar'),
]

# Gestion Auto Asignar Pedido
urlpatterns += [
    url(r'^ws/cancelado/$', views.WsPedidoCancelado.as_view(), name='wspedidocanceladofinal'),
    url(r'^ws/reactivar/$', views.WsPedidoReactivar.as_view(), name='wspedidoreactivar'),
]

# Gestion de Consulta de pedido
urlpatterns += [
    url(r'^info/pedido/cliente/$', TemplateView.as_view(template_name='pedido/pedidoinfo.html'), name='info_pedido_cliente'),
    url(r'^ws/info/pedido/$', views.WsInfoPedido.as_view(), name='ws_info_pedido'),
]
