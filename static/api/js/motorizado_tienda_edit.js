$(document).on('ready',function(){
    if ($('#id_tienda').val().length > 0){
        var tienda = $('#id_tienda').val();
        getSupervisor(tienda);
        getAlistador(tienda);
        getMotorizado(tienda);
    }
    mensajem = $("#menm").dialog({
        autoOpen: false,
        draggable: false,
        modal: true,
        show: {
            effect: "drop",
            direction: "up",
            duration: 500
        },
        hide: {
            effect: "drop",
            direction: "up",
            duration: 500
        },
        buttons: {
            "Ok": function() {
                $(this).dialog("close");
            }
        }
    });
    mensajea = $("#mena").dialog({
        autoOpen: false,
        draggable: false,
        modal: true,
        show: {
            effect: "drop",
            direction: "up",
            duration: 500
        },
        hide: {
            effect: "drop",
            direction: "up",
            duration: 500
        },
        buttons: {
            "Ok": function() {
                $(this).dialog("close");
            }
        }
    });
    mensajes = $("#mens").dialog({
        autoOpen: false,
        draggable: false,
        modal: true,
        show: {
            effect: "drop",
            direction: "up",
            duration: 500
        },
        hide: {
            effect: "drop",
            direction: "up",
            duration: 500
        },
        buttons: {
            "Ok": function() {
                $(this).dialog("close");
            }
        }
    });
    $('#id_tienda').on('change',function(event){
        limpiarSelect();
        if($(this).val().length > 0){
            getSupervisor($(this).val());
            getAlistador($(this).val());
            getMotorizado($(this).val());
        }
    });
});

function limpiarSelect(){
    $('select[name="motorizado"]').html("");
    $('select[name="motorizado"]').html("<option value>Motorizado</option>");
    $('select[name="alistador"]').html("");
    $('select[name="alistador"]').html("<option value>---------</option>");
    $('select[name="supervisor"]').html("");
    $('select[name="supervisor"]').html("<option value>---------</option>");
}

function getMotorizado(t){
    var motorizado = $('select[name="motorizado"]').val();
    $('select[name="motorizado"]').html("");
    $('select[name="motorizado"]').html("<option value>Motorizado</option>");
    $.ajax({
        url:"/motorizado/ws/list/motorizado/?q="+t+"&page=1",
        type:'get',
        dataType:'json',
        success:function(data){
            var r = data.object_list;
            if (r.length > 0){
                for (var key in r){
                    var nom = r[key].nombre,
                        ident = r[key].id_m;
                    $('select[name="motorizado"]').append("<option value=\""+ident+"\""+(String(ident)==motorizado?"selected":"")+">"+nom+"</option>");
                }
            }else{
                mensajem.dialog('open');
            }
        }
    });
}

function getSupervisor(t){
    var supervisor = $('select[name="supervisor"]').val();
    $('select[name="supervisor"]').html("");
    $('select[name="supervisor"]').html("<option value>---------</option>");
    $.ajax({
        url:"/usuario/ws/list/supervisor/?q="+t+"&page=1",
        type:'get',
        dataType:'json',
        success:function(data){
            var r = data.object_list;
            if (r.length > 0){
                for (var key in r){
                    var nom = r[key].nombre,
                        ident = r[key].ident;
                    $('select[name="supervisor"]').append("<option value=\""+ident+"\""+(String(ident)==supervisor?"selected":"")+">"+nom+"</option>");
                }
            }else{
                mensajes.dialog('open');
            }
        }
    });
}

function getAlistador(t){
    var alistador = $('select[name="alistador"]').val();
    $('select[name="alistador"]').html("");
    $('select[name="alistador"]').html("<option value>---------</option>");
    $.ajax({
        url:"/usuario/ws/list/alistador/?q="+t+"&page=1",
        type:'get',
        dataType:'json',
        success:function(data){
            var r = data.object_list;
            if (r.length > 0){
                for (var key in r){
                    var nom = r[key].nombre,
                        ident = r[key].ident;
                    $('select[name="alistador"]').append("<option value=\""+ident+"\""+(String(ident)==alistador?"selected":"")+">"+nom+"</option>");
                }
            }else{
                mensajea.dialog('open');
            }
        }
    });
}
