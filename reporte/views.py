# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from exp.decorators import supervisor_required, administrador_required
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from usuario import models as mod_usuario
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
from reportlab.lib import colors
import json as simplejson
from datetime import date
import csv
from django.views.generic import TemplateView
import forms
from usuario import models as mod_usuario


class Pedido(View):

    def get(self, request):
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', False)
        cursor = connection.cursor()
        cursor.execute('select reporte_pedidos(%d,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer)' % (
            request.user.id, busqueda, order, start, length))
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end class


class Reporte(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        return render(request, 'reporte/index.html')
    # end def
# end class


class Empleados(FormView):

    def get(self, request):
        empresa = mod_usuario.Empresa.objects.filter(
            empleado__id=request.user.id).first()
        e = None
        if empresa:
            e = mod_usuario.Empleado.objects.filter(empresa=empresa).order_by(
                'first_name', 'last_name')
        # end if
        return render(request, 'reporte/empleados.html', {'empleados': e})
    # end def
# end class


class TablaEmpleado(View):
    def get(self, request):
        id_tra = request.GET.get('id_emp', '0')
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', False)
        cursor = connection.cursor()
        m = 'select reporte_tiempos_empleados(%s,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer,%s::integer)' % (
            id_tra, busqueda, order, start, length, request.user.id)
        cursor.execute(m)
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end class
# end class


class TablaInfoEmpleado(View):
    def get(self, request):
        id_tra_tipo = request.GET.get('id_emp_tipo', '')
        id_ciudad = request.GET.get('ciudad', '')
        length = request.GET.get('length', '0')
        columnas = ['nombre', 'descripcion']
        num_columno = request.GET.get('order[0][column]', '0')
        order = request.GET.get('order[0][dir]', 0)
        busqueda = request.GET.get('columns[1][search][value]', '')
        start = request.GET.get('start', 0)
        search = request.GET.get('search[value]', False)
        estado = request.GET.get('estado', 0)
        tienda = request.GET.get('tienda', 0)
        cursor = connection.cursor()
        m = 'select tabla_info_empleado_actualizado(%s,\'%s\'::text,\'%s\'::text,%s::integer,%s::integer,\'%s\'::text,\'%s\'::text,%s::integer)' % (
            request.user.id if request.user.id else 0, busqueda, order, start, length, id_ciudad, id_tra_tipo, tienda)
        cursor.execute(m)
        row = cursor.fetchone()
        return HttpResponse(row[0], content_type="application/json")
    # end def
# end class


class Pdf(View):
    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Reporte_Empleado.pdf'
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        # return (array_to_json(array_agg(row_to_json(row(b,res)))));
        # Header
        print request.GET
        id_emp = request.GET.get('id', '0')
        ini = request.GET.get('ini', '2015-01-01')
        fin = request.GET.get('fin', '%s-%s-%s' %
                              (date.today().year, date.today().month, date.today().day))
        estado = request.GET.get('estado', False)
        # CURSOR DE LA INFO EMPLEADO
        cursor = connection.cursor()
        consulta = 'select get_info_empleados_report_act(%s,\'%s\',\'%s\',%s)' % (id_emp, ini, fin,'true' if estado else 'false')
        print consulta
        cursor.execute(consulta)
        #cursor.execute('select get_info_empleados_report(18,\'2016-05-04\',\'2016-05-04\')')
        row = cursor.fetchone()
        res = row[0]
        #
        if len(res) > 0:
            trab = res[0]['f1'][0]
            c.setLineWidth(.3)
            c.setFont('Helvetica', 22)
            c.drawString(30, 750, trab['nom'])
            c.drawString(30, 730, trab['iden'])
            c.drawString(30, 710, trab['correo'])
            c.drawString(30, 686, trab['tel'])
            response[
                'Content-Disposition'] = 'attachment; filename=Empleado %s.pdf' % trab['nom']
            """c.setFont('Helvetica',12)c.drawString(30,735,'Report')"""
            c.setFont('Helvetica-Bold', 12)
            c.drawString(480, 750, '%s/%s/%s' %
                         (date.today().day, date.today().month, date.today().year))
            c.line(460, 747, 560, 747)

            emp = res[0]['f2']
            # cuerpo de la tabla

            # Table header
            styles = getSampleStyleSheet()
            styleBH = styles["Normal"]
            styles.alingnment = TA_CENTER
            styleBH.fontSize = 9

            cliente = Paragraph('''Cliente''', styleBH)
            direccion = Paragraph('''Direccion''', styleBH)
            total = Paragraph('''Total''', styleBH)
            motorizado = Paragraph('''Motorizado''', styleBH)
            alistar = Paragraph('''Alistami(Min)''', styleBH)
            despacho = Paragraph('''Despacho(Min)''', styleBH)
            entrega = Paragraph('''Entrega(Min)''', styleBH)

            data = []
            data.append([cliente, direccion, total, motorizado,
                         alistar, despacho, entrega])

            # table
            styleN = styles["BodyText"]
            styleN.alingnment = TA_CENTER
            styleN.fontSize = 7

            high = 650
            for student in emp:
                this_student = [student['cliente'][0:15], student['direccion'][0:15], student['total'], student[
                    'motori'][0:15], student['alistar'], student['despacho'], student['entrega']]
                data.append(this_student)
                high = high - 18
            # end for

            width, height = A4
            table = Table(data, colWidths=[
                          3 * cm, 3 * cm, 2 * cm, 3 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm])
            table.setStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ])
            table.wrapOn(c, width, height)
            table.drawOn(c, 30, high)
        else:
            c.drawString(30, 750, 'Empleado no registrado')
        # end if
        c.showPage()  # save page
        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    # end class
# end class


class Excel(View):
    def get(self, request):
        id_emp = request.GET.get('id', '0')
        ini = request.GET.get('inicio', '2015-01-01')
        fin = request.GET.get('fin', '%s-%s-%s' %
                              (date.today().year, date.today().month, date.today().day))
        estado = request.GET.get('estado', False)
        # CURSOR DE LA INFO EMPLEADO
        cursor = connection.cursor()
        cursor.execute(
                    'select get_info_empleados_report_act(%s,\'%s\',\'%s\',%s)' % (id_emp, ini, fin,'true' if estado else 'false'))

        row = cursor.fetchone()
        res = row[0]
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Reporte Empleado.csv"'
        #
        writer = csv.writer(response)
        if len(res) > 0:
            response[
                'Content-Disposition'] = 'attachment; filename="Reporte Empleado.csv"'
            writer = csv.writer(response)
            trab = res[0]['f1'][0]
            writer.writerow(['Nombre Empleado', trab['nom']])
            writer.writerow(['Identificación', trab['iden']])
            writer.writerow(['Correo', trab['correo']])
            writer.writerow(['Telefono', trab['tel']])
            emp = res[0]['f2']
            writer.writerow(['Cliente', 'Direccion', 'Total', 'Motorizado',
                             'Alistamiento(Min)', 'Despacho(Min)', 'Entrega(Min)'])
            for res in emp:
                writer.writerow([res['cliente'], res['direccion'], res['total'], res[
                                'motori'], res['alistar'], res['despacho'], res['entrega']])
            # end def

        else:
            writer.writerow(['Trabajador no encontrado'])
        # end if
        return response

    # end def
# end class


class TiempoEmpleado(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        ciudad = forms.CiudadForm()
        ciudad.fields['ciudad'].queryset = mod_usuario.Ciudad.objects.filter(empresa__empleado__id=request.user.id, status=True)
        return render(request, 'reporte/tipoempleado.html', {'form': ciudad})
    # end def
# end class
