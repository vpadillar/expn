import threading
import time
import httplib
import urllib
from socket import error as socket_error
from . import models


class SendResponseEmpresa(threading.Thread):
    def __init__(self, name, data, host, url, tienda):
        threading.Thread.__init__(self)
        self.name = name
        self.data = data
        self.host = host
        self.url = url
        self.tienda = tienda
    # end def

    def run(self):
        time.sleep(3)
        try:
            parametros = urllib.urlencode(self.data)
            cabeceras = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            abrir_conexion = httplib.HTTPConnection(self.host)
            abrir_conexion.request("POST", self.url, parametros, cabeceras)
            respuesta = abrir_conexion.getresponse()
            # print respuesta.status
            ver_source = respuesta.read()
            res = models.LogEnvio(tienda=self.tienda, status=respuesta.status, response=ver_source, data=self.data)
            res.save()
            # print ver_source
            abrir_conexion.close()
        except socket_error as serr:
            res = models.LogEnvio(tienda=self.tienda, status='500', response='No existe respuesta de la tienda', data=self.data)
            res.save()
        # end try
    # end def
# end class
