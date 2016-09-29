from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import django
from exp.decorators import *
from usuario import models as usuario
from pedido import models as mod_pedido
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.views.generic import TemplateView
import models
import forms
from supra import views as supra
from django.views.generic import View
from usuario import models as usuario
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from usuario import models as usuario
from django.core.exceptions import PermissionDenied
from exp.decorators import administrador_required, supervisor_required
from exp import settings
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from . import models
from django.db.models import Q
from exp.settings import HOST_NODE, PORT_NODE


@login_required(login_url=settings.LOGIN_URL)
def add_motorizado(request):
    user = models.Empleado.objects.filter(username=request.user).first()
    empresa = usuario.Empresa.objects.filter(first_name=user.empresa).first()
    motosC = models.Moto.objects.filter(empresaM=empresa).filter(
        motorizado__moto__isnull=True).count()
    empleadosC = usuario.Empleado.objects.filter(cargo='MOTORIZADO').filter(
        empresa=empresa, motorizado__empleado__isnull=True).count()
    if motosC > 0:
        return redirect(reverse('motorizado:asignar_moto'))
    else:
        if empleadosC > 0:
            if request.method == 'POST':
                formMoto = forms.AddMotoApiForm(
                    request.POST, instance=models.Moto())
                formSoat = forms.AddSoatForm(
                    request.POST, instance=models.Soat())
                formTecno = forms.AddTecnoForm(
                    request.POST, instance=models.Tecno())
                formMotorizado = forms.AddMotorizadoForm(
                    request.POST, instance=models.Motorizado())
                if formSoat.is_valid() and formTecno.is_valid() and formMoto.is_valid() and formMotorizado.is_valid():
                    new_soat = formSoat.save()
                    new_tecno = formTecno.save()
                    new_moto = formMoto.save(commit=False)
                    new_moto.tecno = new_tecno
                    new_moto.soat = new_soat
                    new_moto.empresaM = empresa
                    new_moto.save()
                    new_motorizado = formMotorizado.save(commit=False)
                    new_motorizado.moto = new_moto
                    new_motorizado.save()
                    mensaje = {
                        'tipo': 'success', 'texto': "Se a registrado un motorizado correctamente"}
                    msg = {'mensaje': mensaje, 'formSoat': formSoat, 'formTecno': formTecno,
                           'formMoto': formMoto, 'formMotorizado': formMotorizado}
                    return render(request, 'motorizado/addMotorizado.html', msg)
            else:
                formMoto = forms.AddMotoApiForm(instance=models.Moto())
                formSoat = forms.AddSoatForm(instance=models.Soat())
                formTecno = forms.AddTecnoForm(instance=models.Tecno())
                formMotorizado = forms.AddMotorizadoApiForm(
                    instance=models.Motorizado())
                formMotorizado.fields["empleado"].queryset = empleadosC = models.Empleado.objects.filter(
                    cargo='MOTORIZADO').filter(empresa=empresa, motorizado__empleado__isnull=True)

            return render(request, 'motorizado/addMotorizado.html',
                          {'formSoat': formSoat, 'formTecno': formTecno, 'formMoto': formMoto, 'formMotorizado': formMotorizado})
        else:
            return render(request, 'motorizado/addMotorizado.html', {'error': 'No hay empleados disponibles para asignarles una moto'})


@login_required(login_url=settings.LOGIN_URL)
@csrf_exempt
def searchMotorizado(request):
    length = request.GET.get('length', '0')
    columnas = ['nombre', 'descripcion']
    num_columno = request.GET.get('order[0][column]', '0')
    order = request.GET.get('order[0][dir]', 0)
    busqueda = request.GET.get('columns[1][search][value]', '')
    start = request.GET.get('start', 0)
    search = request.GET.get('search[value]', False)
    cursor = connection.cursor()
    cursor.execute('select tabla_motorizado(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
        request.user.id, busqueda, order, start, length))
    row = cursor.fetchone()
    return HttpResponse(row[0], content_type="application/json")
# end def


@login_required(login_url=settings.LOGIN_URL)
def editMotorizado(request, motorizado_id):
    motorizado = get_object_or_404(models.Motorizado, pk=motorizado_id)
    if request.method == 'POST':
        formMotorizado = forms.editMotorizadoForm(
            request.POST, instance=motorizado)
        if formMotorizado.is_valid():
            formMotorizado.save()
            motorizados = models.Motorizado.objects.filter(
                empleado__id=request.user.id)
            mensaje = {'tipo': 'success',
                       'texto': "Se a editado un motorizado correctamente", 'host_node': '%s:%d' % (HOST_NODE, PORT_NODE)}
            return render(request, 'motorizado/motorizado.html', {'mensaje': mensaje, 'motorizados': motorizados})
    else:
        emp = usuario.Empresa.objects.filter(
            empleado__id=request.user.id).values('first_name').first()
        emp = emp['first_name'] if emp else False
        formMotorizado = forms.editMotorizadoForm(instance=motorizado)
    # end if
    return render(request, 'motorizado/editMotorizado.html', {'form': formMotorizado, 'empresa': emp, 'motorizado': motorizado_id})
# end def


@login_required(login_url=settings.LOGIN_URL)
def infoMoto(request, moto_id):
    moto = get_object_or_404(models.Moto, pk=moto_id)
    soat = models.Soat.objects.get(numeroS=moto.soat)
    tecno = models.Tecno.objects.get(numeroT=moto.tecno)
    return render(request, 'motorizado/infoMoto.html', {'moto': moto, 'soat': soat, 'tecno': tecno})
# end def


class MotoAdd(View):

    def get(self, request):
        formMoto = forms.AddMotoApiForm(instance=models.Moto())
        formSoat = forms.AddSoatForm(instance=models.Soat())
        formTecno = forms.AddTecnoForm(instance=models.Tecno())
        return render(request, 'motorizado/addMoto.html', {'formSoat': formSoat, 'formTecno': formTecno, 'formMoto': formMoto})
    # end def

    def post(self, request):
        formMoto = forms.AddMotoApiForm(request.POST, instance=models.Moto())
        formSoat = forms.AddSoatForm(request.POST, instance=models.Soat())
        formTecno = forms.AddTecnoForm(request.POST, instance=models.Tecno())
        if formSoat.is_valid() and formTecno.is_valid() and formMoto.is_valid():
            new_soat = formSoat.save()
            new_tecno = formTecno.save()
            new_moto = formMoto.save(commit=False)
            new_moto.tecno = new_tecno
            new_moto.soat = new_soat
            new_moto.empresaM = usuario.Empresa.objects.filter(
                empleado__id=request.user.id).first()
            new_moto.save()
            mensaje = {'tipo': 'success',
                       'texto': "Se a registrado una moto correctamente"}
            return render(request, 'motorizado/index.html', {'mensaje': mensaje})
        # end if
        return render(request, 'motorizado/addMoto.html', {'formSoat': formSoat, 'formTecno': formTecno, 'formMoto': formMoto})
# end class


class AsignarMoto(View):

    def get(self, request, *args, **kwargs):
        empleadosC = usuario.Empleado.objects.filter(
            cargo='MOTORIZADO', motorizado__empleado__isnull=True, empresa__empleado__id=request.user.id)
        motosC = models.Moto.objects.filter(
            motorizado__moto__isnull=True, estado=True, empresaM__empleado__id=request.user.id)
        if empleadosC and motosC:
            form = forms.AsignarMotoForm()
            form.fields['moto'].queryset = motosC
            form.fields['empleado'].queryset = empleadosC
            return render(request, 'motorizado/asignarMoto.html', {'form': form})
        # end if
        error = "No hay motos disponibles  para ser asignadas" if motosC is None else "No hay empleados disponibles para ser asignados"
        return render(request, 'motorizado/asignarMoto.html', {'error': error})
    # end def

    def post(self, request, *args, **kwargs):
        form = forms.AsignarMotoForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = {'tipo': 'success',
                       'texto': "Se a asignado una moto correctamente"}
            return render(request, 'motorizado/index.html', {'mensaje': mensaje})
        # end if
        form.fields['empleado'].queryset = usuario.Empleado.objects.filter(
            cargo='MOTORIZADO', motorizado__empleado__isnull=True, empresa__empleado__id=request.user.id)
        form.fields['moto'].queryset = models.Moto.objects.filter(
            motorizado__moto__isnull=True, estado=True, empresaM__empleado__id=request.user.id)
        return render(request, 'motorizado/asignarMoto.html', {'form': form})
    # end def
# end class


@login_required(login_url=settings.LOGIN_URL)
@csrf_exempt
def ListMoto(request):
    length = request.GET.get('length', '0')
    columnas = ['nombre', 'descripcion']
    num_columno = request.GET.get('order[0][column]', '0')
    order = request.GET.get('order[0][dir]', 0)
    busqueda = request.GET.get('columns[1][search][value]', '')
    start = request.GET.get('start', 0)
    search = request.GET.get('search[value]', False)
    cursor = connection.cursor()
    cursor.execute('select tabla_moto(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
        request.user.id if request.user.id else 0, busqueda, order, start, length))
    row = cursor.fetchone()
    return HttpResponse(row[0], content_type="application/json")
# end def


class EditMoto(View):

    def get(self, request, *args, **kwargs):
        moto = get_object_or_404(models.Moto, pk=kwargs['pk'])
        soat = models.Soat.objects.filter(numeroS=moto.soat).first()
        tecno = models.Tecno.objects.filter(numeroT=moto.tecno).first()
        formMoto = forms.AddMotoForm(instance=moto)
        formSoat = forms.AddSoatForm(instance=soat)
        formTecno = forms.AddTecnoForm(instance=tecno)
        return render(request, 'motorizado/editMoto.html', {'formSoat': formSoat, 'formTecno': formTecno, 'formMoto': formMoto, 'pk': kwargs['pk']})
    # end def

    def post(self, request, *args, **kwargs):
        moto = get_object_or_404(models.Moto, pk=kwargs['pk'])
        soat = models.Soat.objects.filter(numeroS=moto.soat).first()
        tecno = models.Tecno.objects.filter(numeroT=moto.tecno).first()
        formMoto = forms.AddMotoApiForm(request.POST, instance=moto)
        formSoat = forms.AddSoatForm(request.POST, instance=soat)
        formTecno = forms.AddTecnoForm(request.POST, instance=tecno)
        empresa = usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        if empresa is None:
            raise PermissionDenied
        # end if
        if formSoat.is_valid() and formTecno.is_valid() and formMoto.is_valid():
            new_soat = formSoat.save()
            new_tecno = formTecno.save()
            new_moto = formMoto.save(commit=False)
            new_moto.tecno = new_tecno
            new_moto.soat = new_soat
            new_moto.estado = True
            new_moto.save()
            mensaje = {'tipo': 'positive',
                       'texto': "Se a editado una moto correctamente"}
            return redirect(reverse('motorizado:index_moto'), mensaje)
        # end if
        return render(request, 'motorizado/editMoto.html', {'formSoat': formSoat, 'formTecno': formTecno, 'formMoto': formMoto, 'pk': kwargs['pk']})
    # end def
# end class


@login_required(login_url=settings.LOGIN_URL)
def DeleteMoto(request, pk):
    moto = get_object_or_404(models.Moto, pk=pk).delete()
    return redirect(reverse('motorizado:list_moto'))
# end class


class SearchMotorizadoPed(View):

    def get(self, request):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', '')
        cursor = connection.cursor()
        cursor.execute('select tabla_pedidos_motorizado(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
            request.user.id if request.user.id else 0, search, order, start, length))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def


class InfoMotorizado(supra.SupraListView):
    model = models.Motorizado
    search_key = 'q'
    list_display = ['identificador', 'nombre', 'apellidos', 'foto']
    search_fields = ['identifier']
    list_filter = ['identifier']
    paginate_by = 1

    class Renderer:
        identificador = 'identifier'
        nombre = 'empleado__first_name'
        apellidos = 'empleado__last_name'
        foto = 'empleado__foto'
    # end class
# end class


class ListMotorizado(supra.SupraListView):
    model = models.Motorizado
    search_key = 'q'
    list_display = ['ident', 'nombre', 'id_m']
    search_fields = ['empleado__tienda__id']
    list_filter = ['empleado__tienda__id']
    paginate_by = 10000

    class Renderer:
        ident = 'empleado__identificacion'
        id_m = 'empleado__usuario_ptr_id'
    # end class

    def nombre(self, obj, row):
        return '%s %s' % (obj.empleado.first_name, obj.empleado.last_name)
    # end def

    def get_queryset(self):
        queryset = super(ListMotorizado, self).get_queryset()
        return queryset.filter(tipo=1)
    # end def
# end class


class ListarRastreo(supra.SupraListView):
    model = models.Motorizado
    search_key = 'q'
    list_display = ['nombre',
                    'identificador', 'placa', ('direccion', 'json'), 'num_pedido', 'tipo']
    search_fields = ['empleado__first_name', 'empleado__last_name',
                     'licencia', 'identifier', 'moto__placa']
    list_filter = ['empleado__first_name', 'empleado__last_name',
                   'licencia', 'identifier', 'moto__placa']
    paginate_by = 10

    class Renderer:
        identificador = 'identifier'
        placa = 'moto__placa'
        direccion = 'empleado__direccion'
    # end class

    def dispatch(self, request, *args, **kwargs):
        return super(ListarRastreo, self).dispatch(request, *args, **kwargs)
    # end def

    def get_queryset(self):
        queryset = super(ListarRastreo, self).get_queryset()

        sql = """
            select (
                select COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
                		select replace(t.direccion,'"','') as direccion,t.num_pedido,t.cliente
                        from (select  replace((cast(cliente as json)::json->'nombre')::text||' '||(cast(cliente as json)::json->'apellidos')::text,'"','') as cliente,id,(cast(cliente as json)::json->'direccion')::text as direccion,
                        case when num_pedido is null or length(num_pedido)=0 then 'pedido_Ws' else num_pedido end as num_pedido  from pedido_pedidows
                        where motorizado_id=m.empleado_id and entregado=false and activado=true and despachado=true
                        union
                        select c.first_name||' '||c.last_name as cliente, p.id, c.direccion as direccion,case when p.num_pedido is not null then p.num_pedido else 'pedido_plataforma' end as num_pedido
                        from pedido_pedido as p inner join usuario_cliente as c on(p.cliente_id=c.id and p.motorizado_id=m.empleado_id and p.entregado=false and p.activado=true and p.despachado=true)) as t
                	) p
                ) as pepidos  from motorizado_motorizado as m where m.empleado_id="motorizado_motorizado"."empleado_id" limit 1
       """
        sql2 = """
           select (
            	select count(t.direccion) as direccion from (select  id,(cast(cliente as json)::json->'direccion')::text as direccion from pedido_pedidows where motorizado_id=m.empleado_id and entregado=false and activado=true and despachado=true
            	union
            	select p.id, c.direccion as direccion from pedido_pedido as p inner join usuario_cliente as c on(p.cliente_id=c.id  and p.motorizado_id=m.empleado_id and p.entregado=false and p.activado=true and p.despachado=true)) as t
            ) as pepidos  from motorizado_motorizado as m where m.empleado_id="motorizado_motorizado"."empleado_id" limit 1
        """
        obj = queryset.extra(select={'direccion': sql, 'num_pedido': sql2})
        empresa = usuario.Empresa.objects.filter(
            empleado__id=self.request.user.id).first()
        return obj.filter(empleado__empresa=empresa)
    # end def

    def nombre(self, obj, row):
        return '%s %s' % (obj.empleado.first_name, obj.empleado.last_name)
    # end def
# end class


class Rastreo(TemplateView):
    template_name = 'motorizado/rastreo.html'

    def dispatch(self, request, *args, **kwargs):
        empresa = models.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        ctx = {'empresa': empresa.id if empresa else 0,
               'token': django.middleware.csrf.get_token(request)}
        return render(request, 'motorizado/rastreo.html', ctx)
    # end def
# end class


class CantidadPedido(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        motorizado = request.POST.get('motorizado', False)
        if motorizado:
            cursor = connection.cursor()
            cursor.execute(
                'select cant_pedidos_motor_periodo(\'%s\')' % motorizado)
            row = cursor.fetchone()
            return HttpResponse('%s' % row[0], content_type='application/json', status=200)
        # end if
        return HttpResponse('0', content_type='application/json', status=200)
    # end def
# end class


class ListNotificaciones(TemplateView):
    template_name = 'motorizado/notificaciones.html'

    def dispatch(self, request, *args, **kwargs):
        # Five days before
        today = date.today()
        this_date_plus_five_days = today + timedelta(days=20)
        expired_soat = models.Moto.objects.filter(soat__fecha_expiracionS__range=[
                                                  today, this_date_plus_five_days], empresaM__empleado__id=request.user.id)
        expired_tecno = models.Moto.objects.filter(tecno__fecha_expiracionT__range=[
                                                   today, this_date_plus_five_days], empresaM__empleado__id=request.user.id)
        return render(request, 'motorizado/notificaciones.html', {'expired_soat': expired_soat, 'expired_tecno': expired_tecno})
    # end def
# end class


class ValidListNotificaciones(supra.SupraListView):
    model = models.Moto
    search_key = 'q'
    list_display = ['tipo']
    search_fields = ['tipo']
    list_filter = ['tipo']
    paginate_by = 100000

    def get_queryset(self):
        queryset = super(ValidListNotificaciones, self).get_queryset()
        today = date.today()
        this_date_plus_five_days = today + timedelta(days=20)
        return queryset.filter(Q(empresaM__empleado__id=self.request.user.id)).filter(
            (Q(soat__fecha_expiracionS__range=[today, this_date_plus_five_days]) |
             Q(tecno__fecha_expiracionT__range=[today, this_date_plus_five_days])))
    # end def
# end class
