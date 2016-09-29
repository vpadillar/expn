var activar;
$(document).on('ready', function() {
    //$("#modal1").show();

    activar = $("#activar").dialog({
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
            "Cancelar": function() {
                $('input[name="pedido"]:checked').prop('checked',false);
                $(this).dialog("close");
            },
            "Aceptar": function() {
                envio();
            }
        }
    });
});

function envio() {
    var id = $('input[name="pedido"]:checked').val();
    if (id != undefined) {
        $.ajax({
            url: '/pedidos/ws/reactivar/',
            data: {
                pedido: id
            },
            dataType: 'json',
            type: 'post',
            success: function(response) {
                window.table.column(1).search($('#search').val()).draw();
                activar.dialog("close");
            }
        });
    }
}

function entrega() {
    var id = $('input[name="ent"]:checked').val();
    if (id != undefined) {
        $.ajax({
            url: '/pedidos/pedido/entrega/update/',
            data: {
                id_ped: id
            },
            dataType: 'json',
            type: 'post',
            success: function(response) {
                window.table.column(1).search($('#search').val()).draw();
                activar.dialog("close");
            }
        });
    }
}
