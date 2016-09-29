from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.conf import settings
from usuario import models as mod_usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.utils.decorators import method_decorator


class Index(View):

    def get(self, request):
        empleado = mod_usuario.Empleado.objects.filter(pk=request.user.id).first()
        if not empleado:
            return redirect_to_login(next=request.get_full_path(), login_url=settings.LOGIN_URL)
        # end if
        request.session["cargo"] = empleado.cargo
        request.session["empresa"] = empleado.empresa.first_name
        if empleado.empresa.first_name == 'Express Del Norte':
            raise PermissionDenied
        else:
            return redirect(reverse('usuario:index_general'))
        # end if
    # end def
# end class
