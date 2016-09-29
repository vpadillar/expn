$(document).on('ready',function(){
    $('#id_ciudad').on('change',function(event){
        var ciudad = $(this).val();
        if(ciudad != undefined){
            $.ajax({
                url:"/usuario/tiendas/ws/?q="+ciudad+"&p=1",
                type:'GET',
                dataType:'json',
                success:function(data){
                    var contenido ="<option value=\"0\">Tienda</option>";
                    var datos = data.object_list;
                    for (var key in data.object_list) {
                        contenido+="<option value=\""+datos[key].id+"\">"+datos[key].nombre+"</option>";
                    }
                    var tienda = $('#tienda');
                    $('#tienda').prop('disabled',false);
                    $('#tienda').html(contenido);
                }
            });
        }else{
            $('#tienda').html('<option value=0>Tienda</>');
            $('#tienda').prop('disabled',true);
        }
    });
});
