from django.core.exceptions import PermissionDenied
from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from usuario.models import Empleado
from django.shortcuts import HttpResponseRedirect


def administrador_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated():
            return redirect_to_login(next=request.get_full_path(), login_url=settings.LOGIN_URL)
        # end if
        empleado1 = Empleado.objects.filter(id=user.id).first()
        print "Entro en esta jajajaj"
        if empleado1:
            if empleado1.cargo == 'ADMINISTRADOR':
                return view_func(request, *args, **kwargs)
            # end if
        # end if
        raise PermissionDenied
    # end def
    return wrapper


def supervisor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        print "Es un alistador"
        if not user.is_authenticated():
            return redirect_to_login(next=request.get_full_path(), login_url=settings.LOGIN_URL)
        # end if
        empleado = Empleado.objects.filter(pk=user.id).first()
        print empleado.cargo
        if empleado.cargo != 'ADMINISTRADOR' and empleado.cargo != 'SUPERVISOR':
            print "entro"
            raise PermissionDenied
        # end if
        print "paso"
        return view_func(request, *args, **kwargs)
    # end def
    return wrapper


def alistador_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated():
            print 'se exploto 7'
            return redirect_to_login(next=request.get_full_path(), login_url=settings.LOGIN_URL)

        id = user.id

        try:
            empleado = Empleado.objects.get(pk=id)
        except ObjectDoesNotExist:
            print 'se exploto 8'
            raise PermissionDenied

        if empleado.cargo != 'ADMINISTRADOR' and empleado.cargo != 'SUPERVISOR' and empleado.cargo != 'ALISTADOR':
            print 'se exploto 9'
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


def motorizado_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated():
            return redirect_to_login(next=request.get_full_path(), login_url=settings.LOGIN_URL)
        # endif
        empleado = Empleado.objects.filter(pk=user.id).first()
        if empleado:
            if empleado.cargo != 'ADMINISTRADOR' and empleado.cargo != 'SUPERVISOR' and empleado.cargo != 'ALISTADOR' and empleado.cargo != 'MOTORIZADO':
                print 'se exploto 12'
                raise PermissionDenied
            # end if
        # end if
        if user.is_authenticated() and user.is_staff and user.is_active:
            return HttpResponseRedirect('/admin/')
        # end if
        return view_func(request, *args, **kwargs)

    return wrapper
