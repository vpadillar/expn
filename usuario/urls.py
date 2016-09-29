from django.conf.urls import patterns, url
import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'login/$', views.custom_login, {'template_name': 'usuario/login.html'}, name='user-login'),
    url(r'logout/$', views.custom_logout, {'next_page': '/', }, name='user-logout'),
]


urlpatterns += [
    url(r'session/$', views.Login.as_view(), name='user-login2'),
    url(r'empleado/$', login_required(TemplateView.as_view(template_name='usuario/index.html')), name='index'),
    url(r'empleado/add/$', login_required(views.EmpleadoAdd.as_view()), name='add_empleado'),
    url(r'empleado/update/states/(?P<empleado_id>\d+)/$', login_required(views.UpStaCliente.as_view()), name='upd_state_empleado'),
    url(r'^empleado/list/$', login_required(TemplateView.as_view(template_name='usuario/empleadoSearch.html')), name='list_empleado'),
    url(r'^empleado/search/$', login_required(views.searchEmpleadoTabla), name='seach_empleado'),
    url(r'^empleado/details/(?P<empleado_id>\d+)/$', views.infoEmpleado, name='details_empleado'),
    url(r'^empleado/edit/(?P<empleado_id>\d+)/$', views.editEmpleado, name='edit_empleado'),
    url(r'^empleado/edit/pass/(?P<pk>\d+)/$', login_required(views.PassChangeEmpleado.as_view(template_name='usuario/passChangeEmpleado.html')), name='edit_pass_empleado'),
    url(r'^$', login_required(views.Index.as_view()), name='index_general'),
]


# Gestion de Clientes
urlpatterns += [
    url(r'^cliente/$', login_required(views.IndexCliente.as_view()), name='index_cliente'),
    url(r'^cliente/add/$', login_required(views.ClienteAdd.as_view()), name='add_cliente'),
    url(r'^cliente/list/$', login_required(TemplateView.as_view(template_name='usuario/clienteSearch.html')), name='list_cliente'),
    url(r'^cliente/search/$', views.searchCliente, name='search_cliente'),
    url(r'^cliente/details/(?P<pk>\d+)/$', login_required(views.DetailCliente.as_view(template_name='usuario/infoCliente.html')), name='details_cliente'),
    url(r'^cliente/edit/(?P<pk>\d+)/$', login_required(views.UpdateCliente.as_view(template_name='usuario/editCliente.html')), name='edit_cliente'),
]

# Gestion de Tienda
urlpatterns += [
    url(r'^tienda/$', login_required(views.IndexTienda.as_view()), name='index_tienda'),
    url(r'^tienda/add/$', login_required(views.AddTienda.as_view()), name='add_tienda'),
    url(r'^tienda/edit/(?P<pk>\d+)/$', login_required(views.UpdateTienda.as_view()), name='update_tienda'),
    url(r'^tienda/details/(?P<pk>\d+)/$', login_required(views.DetailTienda.as_view()), name='details_tienda'),
    url(r'^tienda/delete/(?P<pk>\d+)/$', login_required(views.DeleteTienda.as_view()), name='delete_tienda'),
    url(r'^tienda/list/$', login_required(views.ListTienda.as_view()), name='list_tienda'),
    url(r'^tienda/list/search/$', login_required(views.TablaTienda.as_view()), name='search_tienda'),
]


# Gestion servicios de autenticacion
urlpatterns += [
    url(r'tiendas/ws/', login_required(views.Store.as_view()), name='get_tiendas'),
]


# Gestion servicios de autenticacion
urlpatterns += [
    url(r'session/', views.Login.as_view(), name='ws_loguin'),
    url(r'logged/', views.is_logged, name="is_logged"),
]

# Gestion listar motorizado
urlpatterns += [
    url(r'^ws/list/supervisor/$', login_required(views.ListSupervisor.as_view()), name='ws_list_super'),
    url(r'^ws/list/alistador/$', login_required(views.ListAlistador.as_view()), name='ws_list_alist'),
]
