# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.urlresolvers import reverse
from supra import views as supra
from django.contrib.auth.decorators import login_required
import re
from django.views.generic import View, DeleteView
from django.views import generic
from . import forms
from . import models
from motorizado import models as mod_motorizado
from usuario import forms as form_usuario
from usuario import models as mod_usuario
from django.views.generic.edit import FormView, CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.views.generic.edit import UpdateView
from django.db.models import Q, Sum
from easy_pdf.views import PDFTemplateView
from django.template.loader import get_template
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from exp.decorators import administrador_required, alistador_required, supervisor_required, motorizado_required
from django.utils.decorators import method_decorator
import json
from socketIO_client import SocketIO, LoggingNamespace
from supra.auths import methods, oauth
from . import service
from exp.settings import HOST_NODE, PORT_NODE


class Despacho(TemplateView):
    template_name = 'pedido/despacharpedido.html'

    def dispatch(self, request, *args, **kwargs):
        return super(Despacho, self).dispatch(request, *args, **kwargs)
    # end def
# end class


class AddPedido(View):

    def get(self, request, *args, **kwargs):
        formP = forms.AddPedidoApiForm()
        formP.fields["alistador"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="ALISTADOR").filter(empresa__empleado__id=request.user.id)
        return render(request, 'pedido/addPedido.html', {'formP': formP})
    # end def
# end class


class AddPedidoAdmin(View):

    def get(self, request, *args, **kwargs):
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        if empresa is None:
            return redirect(reverse('pedidos:index_pedido'))
        # end if
        formC = form_usuario.AddClienteForm()
        formP = forms.AddPedidoAdminApiForm(num_pedido=empresa.id)
        formP.fields["alistador"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="ALISTADOR").filter(empresa=empresa)
        formP.fields['tienda'].queryset = mod_usuario.Tienda.objects.filter(
            empresa=empresa)
        formP.fields["supervisor"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="SUPERVISOR").filter(empresa=empresa)
        motori = mod_motorizado.Motorizado.objects.filter(
            empleado__empresa=empresa, tipo=1)
        return render(request, 'pedido/addPedidoAdmin.html',
                      {'formC': formC, 'formP': formP, 'motorizados': motori, 'motorizadosE': []})
    # end def

    def post(self, request, *args, **kwargs):
        print 'Llego 1'
        motorizado = mod_usuario.Empleado.objects.filter(
            identificacion=request.POST['motorizado']).first()
        if motorizado:
            formP = forms.AddPedidoAdminApiForm(request.POST)
            empresa = mod_usuario.Empresa.objects.filter(
                empleado__id=request.user.id).first()
            if formP.is_valid():
                form = formP.save(commit=False)
                form.motorizado = motorizado
                form.empresa = empresa
                form.activado = True
                form.save()
                cursor = connection.cursor()
                cursor.execute('select get_add_pedido_admin(%d)' % form.id)
                row = cursor.fetchone()
                return redirect(reverse('pedido:add_item_pedido', kwargs={'pk': form.id}))
            # end if
        # end if
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        if empresa is None:
            return redirect(reverse('pedido:index_pedido'))
        # end if
        formC = form_usuario.AddClienteForm()
        formP.fields["alistador"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="ALISTADOR").filter(empresa=empresa)
        formP.fields["supervisor"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="SUPERVISOR").filter(empresa=empresa)
        motori = mod_motorizado.Motorizado.objects.filter(
            empleado__empresa=empresa, tipo=1)
        formP.fields['tienda'].queryset = mod_usuario.Tienda.objects.filter(
            empresa=empresa)
        info = {'formC': formC, 'formP': formP,
                'motorizados': motori,
                'motorizadosE': []}
        return render(request, 'pedido/addPedidoAdmin.html', info)
    # end def
# end class


class EditPedido(FormView):

    def get(self, request, *args, **kwargs):
        pedido = get_object_or_404(models.Pedido, id=kwargs['pk'])
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        if empresa:
            pedidoForm = forms.EditPedidoAdminApiForm(instance=pedido)
            pedidoForm.fields["alistador"].queryset = mod_usuario.Empleado.objects.filter(
                cargo="ALISTADOR").filter(empresa=empresa)
            pedidoForm.fields['tienda'].queryset = mod_usuario.Tienda.objects.filter(
                empresa=empresa)
            pedidoForm.fields["supervisor"].queryset = mod_usuario.Empleado.objects.filter(
                cargo="SUPERVISOR").filter(empresa=empresa)
            motorizado = mod_motorizado.Motorizado.objects.filter(
                empleado__empresa=empresa).values_list('id', flat=True)
            pedidoForm.fields["motorizado"].queryset = mod_usuario.Empleado.objects.filter(
                cargo="MOTORIZADO").filter(empresa=empresa, motorizado__id__in=motorizado)
            return render(request, 'pedido/editPedido.html', {'pedidoForm': pedidoForm})
        # end if
        return redirect(reverse('pedido:index_pedido'))
    # end def

    def post(self, request, *args, **kwargs):
        pedido = get_object_or_404(models.Pedido, id=kwargs['pk'])
        motor_ant = pedido.motorizado.motorizado.identifier
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        pedidoForm = forms.EditPedidoAdminApiForm(
            request.POST, instance=pedido)
        if pedidoForm.is_valid() and empresa:
            f = pedidoForm.save(commit=False)
            f.empresa = empresa
            f.save()
            models.Pedido.objects.filter(id=pedido.id).update(activado=True)
            motor_sig = f.motorizado.motorizado.identifier
            print motor_ant, motor_sig
            if motor_ant != motor_sig:
                cursor = connection.cursor()
                cursor.execute(
                    'select get_add_pedido_admin(%d)' % pedido.id)
                row = cursor.fetchone()
                lista = row[0]
                if lista:
                    with SocketIO(HOST_NODE, PORT_NODE, LoggingNamespace) as socketIO:
                        socketIO.emit('modificar-motorizado-pedido', {
                            'pedido': lista[0], 'tipo': 1, 'retraso': lista[0]['retraso'], 'mot_anterior': motor_ant, 'mot_siguiente': motor_sig})
                        socketIO.wait(seconds=0)
                    # end with
                # end if
            # end if
            return redirect(reverse('pedido:add_item_pedido', kwargs={'pk': f.id}))
        # end if
        pedidoForm.fields['tienda'].queryset = mod_usuario.Tienda.objects.filter(
            empresa=empresa)

        pedidoForm.fields["alistador"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="ALISTADOR").filter(empresa=empresa)
        pedidoForm.fields['tienda'].queryset = mod_usuario.Tienda.objects.filter(
            empresa=empresa)
        pedidoForm.fields["supervisor"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="SUPERVISOR").filter(empresa=empresa)
        motorizado = mod_motorizado.Motorizado.objects.filter(
            empleado__empresa=empresa).values_list('id', flat=True)
        pedidoForm.fields["motorizado"].queryset = mod_usuario.Empleado.objects.filter(
            cargo="MOTORIZADO").filter(empresa=empresa, motorizado__id__in=motorizado)
        return render(request, 'pedido/editPedido.html', {'pedidoForm': pedidoForm})
    # end def

# end class


class AddItemPedido(View):

    def get(self, request, *args, **kwargs):
        total = 0
        pedido = get_object_or_404(models.Pedido, pk=kwargs['pk'])
        items = models.ItemsPedido.objects.filter(
            pedido=pedido).select_related('item')
        if items:
            resul = items.aggregate(suma=Sum('valor_total'))
            total = resul['suma'] if resul['suma'] is not None else 0
        # end if
        formItems = forms.AddItemsPedidoForm()
        formItems.fields["item"].queryset = models.Items.objects.filter(
            empresaI=pedido.empresa, status=True)
        return render(request, 'pedido/pedidoItems.html', {'pedido': pedido, 'items': items, 'form': formItems, 'total': total})
    # end def

    def post(self, request, *args, **kwargs):
        total = 0
        pedido = get_object_or_404(models.Pedido, pk=kwargs['pk'])
        items = models.ItemsPedido.objects.filter(
            pedido=pedido).select_related('item')
        if items:
            resul = items.aggregate(suma=Sum('valor_total'))
            total = resul['suma'] if resul['suma'] is not None else 0
        formItems = forms.AddItemsPedidoForm(request.POST)
        print "llego"
        if formItems.is_valid():
            formI = formItems.save(commit=False)
            print "llego a la vaina  %d %d" % (formI.valor_unitario, formI.cantidad)
            if formI.valor_unitario > 0 and formI.cantidad > 0:
                formI.pedido = pedido
                formI.valor_total = formI.valor_unitario * formI.cantidad
                formI.save()
                return redirect(reverse('pedido:add_item_pedido', kwargs={'pk': pedido.id}))
        # end if
        formItems.fields["item"].queryset = models.Items.objects.filter(
            empresaI=pedido.empresa, status=True)
        return render(request, 'pedido/pedidoItems.html',
                      {'pedido': pedido, 'form': formItems, 'items': items, 'total': total})
        # end if
    # end def
# end class


class FinalizarPedido(View):

    def post(self, request, *args, **kwargs):
        if kwargs['pk']:
            pedido = models.Pedido.objects.filter(id=kwargs['pk']).first()
            if pedido:
                items = models.ItemsPedido.objects.filter(pedido=pedido)
                if items:
                    resul = items.aggregate(suma=Sum('valor_total'))
                    total = resul['suma'] if resul['suma'] is not None else 0
                    if total > 0:
                        models.Pedido.objects.filter(id=kwargs['pk']).update(
                            total=total, confirmado=True)
                        cursor = connection.cursor()
                        cursor.execute(
                            'select get_add_pedido_admin(%d)' % pedido.id)
                        row = cursor.fetchone()

                        lista = row[0]
                        if lista:
                            if not pedido.confirmado:
                                with SocketIO(HOST_NODE, PORT_NODE, LoggingNamespace) as socketIO:
                                    socketIO.emit('modificar-pedido', {
                                                  'pedido': lista[0], 'tipo': 1, 'retraso': lista[0]['retraso']})
                                    socketIO.wait(seconds=0)
                                # end with
                            else:
                                with SocketIO(HOST_NODE, PORT_NODE, LoggingNamespace) as socketIO:
                                    socketIO.emit('modificar-pedido', {
                                                  'pedido': lista[0], 'tipo': 1, 'retraso': lista[0]['retraso']})
                                    socketIO.wait(seconds=0)
                                # end with
                            # end if
                        # end if
                        return redirect(reverse('pedido:list_pedido'))
                    # end if
                # end if
                error = "No puedes dejar el pedido sin items."
                formItems = forms.AddItemsPedidoForm()
                formItems.fields["item"].queryset = models.Items.objects.filter(
                    empresaI=pedido.empresa, status=True)
                return render(request, 'pedido/pedidoItems.html', {'pedido': pedido, 'items': items, 'form': formItems, 'total': 0, 'error': error})
            # end if
        # end if
        return PermissionDenied
    # end if
# end if


class AddItem(CreateView):
    form_class = forms.AddItemsForm
    model = models.Items
    template_name = 'pedido/addItems.html'

    def post(self, request, *args, **kwargs):
        f = forms.AddItemsApiForm(request.POST)
        if f.is_valid():
            form = f.save(commit=False)
            empresa = models.Empresa.objects.filter(
                empleado__id=request.user.id).first()
            form.empresaI = empresa
            form.status = True
            mensaje = {'tipo': 'success',
                       'texto': 'El item se agregó correctamente'}
            form.save()
            return render(request, 'pedido/addItems.html', {'form': forms.AddItemsApiForm(), 'mensaje': mensaje})
        # end if
        return render(request, 'pedido/addItems.html', {'form': f})
    # end def
# end class


class TablaItems(View):

    @method_decorator(csrf_exempt)
    def get(self, request):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = int(request.GET.get('start', 0))
        search = request.GET.get('search[value]', False)
        cursor = connection.cursor()
        m = 'select tabla_items(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
            request.user.id, busqueda, order, start, length)
        cursor.execute(m)
        row = cursor.fetchone()
        print row
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end def


class UpdateItem(UpdateView):
    model = models.Items
    form_class = forms.AddItemsApiForm
    template_name = 'pedido/editItems.html'

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(models.Items, pk=kwargs['pk'])
        form = forms.AddItemsApiForm(request.POST, instance=item)
        if form.is_valid():
            form.instance.status = True
            form.save()
            mensaje = {'tipo': 'success',
                       'texto': 'El item se actualizó correctamente'}
            return render(request, 'pedido/editItems.html', {'mensaje': mensaje, 'form': form})
        # end if
        return render(request, 'pedido/editItems.html', {'form': form})
# end class


class DeleteItemPedido(DeleteView):
    models = models.ItemsPedido

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(models.ItemsPedido, pk=kwargs['pk'])
        item.delete()
        return redirect(reverse('pedido:add_item_pedido', kwargs={'pk': kwargs['id_pedido']}))
# end class


class TablaPedido(View):

    def get(self, request, *args, **kwargs):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', False)
        cursor = connection.cursor()
        cursor.execute('select tabla_pedidos(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
            request.user.id, busqueda, order, start, length))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end class


class TablaDespachoPedido(View):

    def get(self, request, *args, **kwargs):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', False)
        cursor = connection.cursor()
        cursor.execute('select tabla_pedidos_despacho(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
            request.user.id, busqueda, order, start, length))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end class


class UpdateServicePedido(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        # do something
        return super(UpdateServicePedido, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        id_pedido = request.POST['id_ped']
        if id_pedido:
            models.Pedido.objects.filter(
                id=int(id_pedido)).update(despachado=True)
            return HttpResponse("true", content_type="application/json")
        # end if
        return HttpResponse("false", content_type="application/json")
    # end class
# end class


class UpdateEntregaServicePedido(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UpdateEntregaServicePedido, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        id_pedido = request.POST['id_ped']
        if id_pedido:
            pedido = models.Pedido.objects.filter(id=int(id_pedido)).first()
            if pedido:
                if pedido.despachado:
                    models.Pedido.objects.filter(
                        id=int(id_pedido)).update(entregado=True)
                    return HttpResponse("true", content_type="application/json")
                # end if
            # end if
        # end if
        return HttpResponse("false", content_type="application/json")
    # end def
# end class


class InfoPedido(FormView):

    def get(self, request, *args, **kwargs):
        pedido = get_object_or_404(models.Pedido, pk=kwargs['pk'])
        items = models.ItemsPedido.objects.filter(pedido=pedido)
        tiempos = models.Time.objects.filter(pedido=pedido).first()
        print tiempos
        return render(request, 'pedido/infoPedido.html', {'pedido': pedido, 'items': items, 'tiempo': tiempos})
    # end def
# end class


class FacturaPedido(PDFTemplateView):
    template_name = "pedido/factura.html"

    def get_context_data(self, **kwargs):
        pedido = get_object_or_404(models.Pedido, pk=kwargs['pk'])
        items = models.ItemsPedido.objects.filter(pedido=pedido)
        empresa = mod_usuario.Empresa.objects.get(first_name=pedido.empresa)
        cliente = mod_usuario.Cliente.objects.get(
            identificacion=pedido.cliente)
        return super(FacturaPedido, self).get_context_data(
            pagesize="A5",
            title="Pedido", pedido=pedido, items=items, empresa=empresa, cliente=cliente,
            **kwargs
        )
    # end def
# end class


class MisPedidos(View):

    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        empleado = get_object_or_404(mod_usuario.Empleado, pk=request.user.id)
        if empleado:
            if empleado.cargo == 'SUPERVISOR' or empleado.cargo == 'ADMINISTRADOR' or empleado.cargo == 'ALISTADOR':
                return render(request, 'pedido/misPedidos.html')
            else:
                return render(request, 'motorizado/pedidosmotorizado.html')
            # end if
        # end if
        raise PermissionDenied

    # end def
# end class


class TablaMisPedidos(View):

    def get(self, request):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', False)
        cursor = connection.cursor()
        cursor.execute('select mis_pedidos_asignados(%d,%s,%s)' %
                       (request.user.id if request.user.id else 0, start, length))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end class


class TablaPedidosAsignar(View):

    def get(self, request):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', False)
        cursor = connection.cursor()
        cursor.execute('select pedidos_a_asignar_motor(%d,%s,%s)' %
                       (request.user.id if request.user.id else 0, start, length))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end class


class AsignarPedidoMotorizado(View):

    @method_decorator(alistador_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)
    # end def

    def get(self, request, *args, **kwargs):
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        if empresa:
            motorizados = mod_motorizado.Motorizado.objects.filter(
                empleado__empresa=empresa)
            return render(request, 'pedido/chooseMotorizado.html', {'motorizados': motorizados, 'motorizadosE': [], 'pedido': kwargs['pedido_id']})
        # end if
        return PermissionDenied
    # end def
# end class


class CAMotorizado(View):

    def post(self, request, *args, **kwargs):
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        if kwargs['pedido_id'] and request.POST['motorizado'] and empresa:
            cursor = connection.cursor()
            cursor.execute('select asignar_motorizado_perr(%s::integer,\'%s\')' % (
                kwargs['pedido_id'], request.POST['motorizado']))
            row = cursor.fetchone()
            if row[0]:
                mensaje = {'tipo': 'success',
                           'texto': 'Se asignó el motorizado correctamente'}
                motorizados = mod_motorizado.Motorizado.objects.filter(
                    empleado__empresa=empresa)
                return render(request, 'pedido/asignarMotorizado.html', {'mensaje': mensaje, 'motorizados': motorizados, 'motorizadosE': [], 'pedido': kwargs['pedido_id']})
            # end if
        # end if
        return PermissionDenied
    # end def
# end class


class UpSerPedido(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UpSerPedido, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        id_pedido = request.POST['id_ped']
        if id_pedido:
            models.Pedido.objects.filter(
                id=int(id_pedido)).update(despachado=True)
            return HttpResponse("true", content_type="application/json")
        # end if
        return HttpResponse("false", content_type="application/json")
    # end class
# end class


class UpdPedSerEntrega(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UpdPedSerEntrega, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        id_pedido = request.POST['id_ped']
        if id_pedido:
            pedido = models.Pedido.objects.filter(id=int(id_pedido)).first()
            if pedido:
                print pedido.despachado, ' Esa es la variable'
                if pedido.despachado:
                    models.Pedido.objects.filter(
                        id=int(id_pedido)).update(entregado=True)
                    return HttpResponse("true", content_type="application/json")
                # end if
            # end if
        # end if
        return HttpResponse("false", content_type="application/json")
    # end def
# end class


class WsPedidoEmpresa(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(WsPedidoEmpresa, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        print request.body.decode('utf-8')
        try:
            resp = json.loads(request.body.decode('utf-8'))['token']
        except:
            return HttpResponse('{"r":"Error en el token"}', content_type="application/json", status=403)
        # end try
        if resp:
            tienda = mod_usuario.Tienda.objects.filter(token=resp).first()
            if tienda:
                cursor = connection.cursor()
                cursor.execute('select ws_add_pedido_service(\'%s\'::json)' %
                               request.body.decode('utf-8'))
                row = cursor.fetchone()
                lista = json.loads(row[0])
                if lista['respuesta']:
                    if len(lista['pedidos']) > 0:
                        with SocketIO(HOST_NODE, PORT_NODE, LoggingNamespace) as socketIO:
                            socketIO.emit('add-pedido', {
                                          'pedidos': lista['pedidos'], 'tipo': 2, 'retraso': lista['retardo']})
                            socketIO.wait(seconds=0)
                        # end with
                        lista.pop('pedidos')
                    # end if
                # end if
                url_ = tienda.url.split('/', 1) if tienda.url is not None or len(tienda.url) > 0 else ["", ""]
                url_ = ["", ""] if len(url_) < 2 else url_
                thead_respose_empresa = service.SendResponseEmpresa('solicitud_Empresa_%d' % tienda.id, lista, url_[0], "/"+url_[1],tienda.id)
                thead_respose_empresa.start()
                return HttpResponse(json.dumps(lista), content_type="application/json")
            # end if
        # end if
        return HttpResponse('{"r":"Error en el token"}', content_type="application/json", status=403)
    # end def
# end class


class Rastreo(TemplateView):
    template_name = 'pedido/rastreo.html'

    @method_decorator(administrador_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Rastreo, self).dispatch(request, *args, **kwargs)
    # end def
# end class


class RecogerPWService(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RecogerPWService, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        pedido = request.POST.get('pedido', False)
        motorizado = request.POST.get('motorizado', False)
        if pedido and motorizado:
            motori = mod_motorizado.Motorizado.objects.filter(
                identifier=motorizado).first()
            if motori:
                if validNum(pedido) and motorizado:
                    ped = models.PedidoWS.objects.filter(
                        id=int(pedido), motorizado__id=motori.empleado.id).first()
                    if ped:
                        models.PedidoWS.objects.filter(
                            id=int(pedido), motorizado__id=motori.empleado.id).update(despachado=True)
                        return HttpResponse('[{"status":true}]', content_type='application/json', status=200)
                # end if
            # end if
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def
# end class


class RecogerPPlataforma(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RecogerPPlataforma, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        pedido = request.POST.get('pedido', False)
        motorizado = request.POST.get('motorizado', False)
        if pedido and motorizado:
            motori = mod_motorizado.Motorizado.objects.filter(
                identifier=motorizado).first()
            if motori:
                if validNum(pedido) and motorizado:
                    ped = models.Pedido.objects.filter(
                        id=int(pedido), motorizado__id=motori.empleado.id).first()
                    if ped:
                        models.Pedido.objects.filter(
                            id=int(pedido), motorizado__id=motori.empleado.id).update(despachado=True)
                        return HttpResponse('[{"status":true}]', content_type='application/json', status=200)
                    # end if
                # end if
            # end if
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def
# end class


class AceptarPWService(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AceptarPWService, self).dispatch(*args, **kwargs)
    # end def

    def get(self, request, *args, **kwargs):
        return HttpResponse('jajjajaja', content_type='application/json')

    def post(self, request, *args, **kwargs):
        pedido = request.POST.get('pedido', False)
        motorizado = request.POST.get('motorizado', False)
        if pedido and motorizado:
            print 'paso 1'
            if validNum(pedido) and motorizado:
                cursor = connection.cursor()
                cursor.execute('select aceptar_pw_service(%s,\'%s\')' %
                               (pedido, motorizado))
                row = cursor.fetchone()
                res = json.loads(row[0])
                return HttpResponse(row, content_type='application/json', status=200 if res['r'] else 404)
            # end if
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def
    # end class


class AceptarPPlataforma(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AceptarPPlataforma, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        motorizado = request.POST.get('motorizado', False)
        pedido = request.POST.get('pedido', False)
        if motorizado and pedido:
            if motorizado and validNum(pedido):
                # mod_usuario.Empleado.objects.filter(ddsdsd=12)
                pedid = models.Pedido.objects.filter(id=int(pedido)).values(
                    'id', 'motorizado__motorizado__identifier', 'motorizado__id').first()
                print pedid
                if pedid:
                    if pedid['motorizado__motorizado__identifier'] == motorizado:
                        models.Pedido.objects.filter(
                            id=int(pedido)).update(notificado=True)
                        return HttpResponse('[{"status":true}]', content_type='application/json', status=200)
                # end if
            # end if
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def

# end class


class EntregarPWService(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        print 'llego a el service'
        return super(EntregarPWService, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        print 'entro a el post'
        pedido = request.POST.get('pedido', False)
        motorizado = request.POST.get('motorizado', False)
        if pedido and motorizado:
            if validNum(pedido) and motorizado:
                ped = models.PedidoWS.objects.filter(
                    id=int(pedido), motorizado__motorizado__identifier=motorizado).values(
                        'id', 'motorizado__motorizado__identifier', 'motorizado__id').first()
                if ped:
                    models.PedidoWS.objects.filter(
                        id=int(pedido)).update(entregado=True)
                    return HttpResponse('[{"status":true}]', content_type='application/json', status=200)
                # end if
            # end if
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def
# end class


class EntregarPPlataforma(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(EntregarPPlataforma, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        pedido = request.POST.get('pedido', False)
        motorizado = request.POST.get('motorizado', False)
        if pedido and motorizado:
            if validNum(pedido) and motorizado:
                ped = models.Pedido.objects.filter(
                    id=int(pedido), motorizado__motorizado__identifier=motorizado).first()
                if ped:
                    models.Pedido.objects.filter(
                        id=int(pedido)).update(entregado=True)
                    return HttpResponse('[{"status":true}]', content_type='application/json', status=200)
                # end if
            # end if
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def
# end class


class ConfirmacionPedido(supra.SupraFormView):

    model = models.ConfirmarPedido

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        motorizado = request.POST.get('motorizado', '')
        pedido = request.POST.get('pedido', 0)
        pedidov = models.Pedido.objects.filter(
            id=pedido, motorizado__motorizado__identifier=motorizado).first()
        if pedidov:
            models.Pedido.objects.filter(id=int(pedido)).update(entregado=True)
            return super(ConfirmacionPedido, self).dispatch(request, *args, **kwargs)
        # end if
        return HttpResponse('{"motorizado":["Este campo es obligatorio"]}')
    # end def
# end class


class ConfirmacionPedidoWS(supra.SupraFormView):

    model = models.ConfirmarPedidoWs

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        motorizado = request.POST.get('motorizado', '')
        pedido = request.POST.get('pedido', 0)
        pedidov = models.PedidoWS.objects.filter(
            id=pedido, motorizado__motorizado__identifier=motorizado).first()
        if pedidov:
            models.PedidoWS.objects.filter(
                id=int(pedido)).update(entregado=True)
            return super(ConfirmacionPedidoWS, self).dispatch(request, *args, **kwargs)
        # end if
        return HttpResponse('{"motorizado":["Este campo es obligatorio"]}')
    # end def
# end class


class AutoAsignar(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AutoAsignar, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        motorizado = request.POST.get('motorizado_json', '[]')
        tienda = request.POST.get('tienda', '0')
        cursor = connection.cursor()
        cursor.execute('select auto_asignar(%s,\'%s\')' % (tienda, motorizado))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end class


class AsignarMotorizado(View):

    @method_decorator(alistador_required)
    def dispatch(self, request, *args, **kwargs):
        return render(request, 'pedido/asignarMotorizado.html')
    # end def
# end class


class CancelarPPlataforma(supra.SupraFormView):
    model = models.CancelarPedido

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        motorizado = request.POST.get('motorizado', '')
        n_pedido = request.POST.get('pedido', 0)
        pedido = models.Pedido.objects.filter(
            id=n_pedido, motorizado__motorizado__identifier=motorizado).first()
        if pedido:
            models.Pedido.objects.filter(
                id=int(n_pedido)).update(activado=False)
            return super(CancelarPPlataforma, self).dispatch(request, *args, **kwargs)
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def

# end class


class CancelarPWService(supra.SupraFormView):
    model = models.CancelarPedidoWs

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        motorizado = request.POST.get('motorizado', '')
        n_pedido = request.POST.get('pedido', 0)
        pedido = models.PedidoWS.objects.filter(
            id=n_pedido, motorizado__motorizado__identifier=motorizado).first()
        if pedido:
            models.PedidoWs.objects.filter(
                id=int(n_pedido)).update(activado=False)
            return super(CancelarPWService, self).dispatch(request, *args, **kwargs)
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def

# end class


class ConfiguracionTiempo(View):

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ConfiguracionTiempo, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        id = request.POST.get('id', "")
        if validNum(id):
            configuracion = get_object_or_404(
                models.ConfiguracionTiempo, pk=int(id))
            form = forms.AddConfiguracion(request.POST, instance=configuracion)
            if form.is_valid():
                addconfi = form.save(commit=False)
                addconfi.empresa = mod_usuario.Empresa.objects.filter(
                    empleado__id=request.user.id).first()
                addconfi.save()
                return redirect(reverse('pedido:configurar_pplataforma'))
            # end if
            return render(request, 'pedido/addConfiguracion.html', {'pk': configuracion.id, 'form': form})
        else:
            form = forms.AddConfiguracion(request.POST)
            if form.is_valid():
                addconfi = form.save(commit=False)
                addconfi.empresa = mod_usuario.Empresa.objects.filter(
                    empleado__id=request.user.id).first()
                addconfi.save()
                return render(request, 'pedido/addConfiguracion.html', {'pk': addconfi.id, 'form': form})
            # end if
            return render(request, 'pedido/addConfiguracion.html', {'form': form})
        # end if
    # end def

    def get(self, request, *args, **kwargs):
        configuracion = models.ConfiguracionTiempo.objects.filter(
            empresa__empleado__id=request.user.id).first()
        if configuracion:
            return render(request, 'pedido/addConfiguracion.html', {'pk': configuracion.id, 'form': forms.AddConfiguracion(instance=configuracion)})
        # end if
        return render(request, 'pedido/addConfiguracion.html', {'form': forms.AddConfiguracion()})
    # end def


class ReactivarPPlataforma(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ReactivarPPlataforma, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        pedido = request.POST.get('pedido', False)
        if pedido:
            if validNum(pedido):
                ped = models.Pedido.objects.filter(
                    id=int(pedido)).first()
                if ped:
                    models.Pedido.objects.filter(
                        id=int(pedido)).update(activado=True)
                    return HttpResponse('[{"status":true}]', content_type='application/json', status=200)
                # end if
            # end if
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def
# end class


class WsPedidoCancelado(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(WsPedidoCancelado, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        pedido = request.POST.get('pedido', False)
        if pedido:
            if validNum(pedido):
                pedido_ = models.Pedido.objects.filter(id=int(pedido)).first()
                if pedido_:
                    models.Pedido.objects.filter(
                        id=int(pedido)).update(activado=False)
                    return HttpResponse('[{"status":true}]', content_type='application/json', status=200)
                # end if
            # end def
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def
# end class


class WsPedidoReactivar(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(WsPedidoReactivar, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        pedido = request.POST.get('pedido', False)
        if pedido:
            if validNum(pedido):
                pedido_ = models.Pedido.objects.filter(id=int(pedido)).first()
                if pedido_:
                    cursor = connection.cursor()
                    cursor.execute(
                        'select reactivar_pedido(%s::integer)' % pedido)
                    row = cursor.fetchone()
                    try:
                        lista = json.loads('%s' % row[0])
                    except:
                        lista = row[0]
                    # end try
                    if lista:
                        with SocketIO(HOST_NODE, PORT_NODE, LoggingNamespace) as socketIO:
                            socketIO.emit('asignar-pedido', {
                                          'pedido': lista[0]['f3'][0], 'tipo': 1, 'retraso': lista[0]['f3'][0]['retraso']})
                            socketIO.wait(seconds=0)
                        # end with
                        return HttpResponse('[{"status":true}]', content_type='application/json', status=200)
                    # end if
                # end if
            # end def
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def


class WsInfoPedido(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(WsInfoPedido, self).dispatch(*args, **kwargs)
    # end def

    def post(self, request, *args, **kwargs):
        pedido = request.POST.get('pedido', False)
        if pedido:
            cursor = connection.cursor()
            cursor.execute(
                'select get_info_pedido_cliente(\'%s\')' % pedido)
            row = cursor.fetchone()
            if row:
                return HttpResponse(row[0], content_type="application/json")
            # end if
        # end if
        return HttpResponse('{"r":false}', content_type="application/json")
    # end def
# end class


def validNum(cad):
    return re.match('^\d+$', cad)
