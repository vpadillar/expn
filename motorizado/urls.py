from django.conf.urls import patterns, url
from django.views.generic import TemplateView
import views
from django.contrib.auth.decorators import login_required


# Gestion de motorizado
urlpatterns = [
    url(r'^motorizado/add/$', views.add_motorizado, name='add_motorizado'),
    url(r'^motorizado/search/$', views.searchMotorizado, name='search_motorizado'),
    url(r'^motorizado/list/$', login_required(TemplateView.as_view(
        template_name='motorizado/motorizado.html')), name='list_motorizado'),
    url(r'^motorizado/edit/(?P<motorizado_id>\d+)/$',
        views.editMotorizado, name='edit_motorizado'),
    url(r'^moto/details/(?P<moto_id>\d+)/$',
        views.infoMoto, name='api_info_moto'),
    url(r'^motorizado/search/pedido/$', login_required(views.SearchMotorizadoPed.as_view()), name='search_pedido_motorizado'),
]

# Gestion de despacho
urlpatterns += [
    url(r'^rastreo/$', login_required(views.Rastreo.as_view()), name='rastreo_motorizado'),
]

# Gestion de Moto
urlpatterns += [
    url(r'^moto/$', login_required(TemplateView.as_view(template_name='motorizado/index.html')),
        name="index_moto"),
    url(r'^moto/add/$', login_required(views.MotoAdd.as_view()), name='add_moto'),
    url(r'^moto/list/$', login_required(TemplateView.as_view(template_name='motorizado/motoSearch.html')), name='list_moto'),
    url(r'^moto/search/$', views.ListMoto, name='search_moto'),
    url(r'^moto/delete/(?P<pk>\d+)/$', views.DeleteMoto, name='delete_moto'),
    url(r'^moto/edit/(?P<pk>\d+)/$', login_required(views.EditMoto.as_view()), name='edit_moto'),
    url(r'^moto/asignar/$', login_required(views.AsignarMoto.as_view()), name='asignar_moto'),

]

# Gestion de Foto += [
urlpatterns += [
    url(r'^motorizado/foto/$', login_required(TemplateView.as_view(template_name='motorizado/foto.html')),
        name='foto_pedido_motorizado'),
    url(r'^text/$', login_required(TemplateView.as_view(template_name='motorizado/text.html')),
        name='text'),
]

# Gestion de Rastreo pedido
urlpatterns += [
    url(r'^ws/list/rastreo/$', login_required(views.ListarRastreo.as_view()), name='listar_rastreo'),

]


# Gestion cantidad de periodos en el periodo actual de quincena
urlpatterns += [
    url(r'^get/info/$', views.InfoMotorizado.as_view(), name='info_motorizado'),
]


# Gestion cantidad de periodos en el periodo actual de quincena
urlpatterns += [
    url(r'^get/pedidos/$', login_required(views.CantidadPedido.as_view()), name='num_pedidos'),

]

# Gestion listar motorizado
urlpatterns += [
    url(r'^ws/list/motorizado/$', views.ListMotorizado.as_view(), name='ws_list_moto'),
]

# Gestion listar motorizado
urlpatterns += [
    url(r'^notificaciones/$', views.ListNotificaciones.as_view(), name='ws_list_noti'),
    url(r'^ws/notificaciones/$', views.ValidListNotificaciones.as_view(), name='ws_valid_list_noti'),
]
