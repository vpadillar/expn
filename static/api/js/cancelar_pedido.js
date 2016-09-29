var dialogo, pedido, cancelar, mensaje;
$(document).on('ready', function() {
    //$("#modal1").show();

    cancelar = $("#cancelar").dialog({
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
                $(this).dialog("close");
            },
            "Aceptar": function() {
                envioCancelar();
            }
        }
    });
    mensaje = $("#men").dialog({
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
});

function envioCancelar() {
    var id = $('input[name="pedido"]:checked').val();
    if (id != undefined){
        $.ajax({
            url: '/pedidos/ws/cancelado/',
            data: {
                pedido: id
            },
            dataType: 'json',
            type: 'post',
            success: function(response) {
                window.table.column(1).search($('#search').val()).draw();
                cancelar.dialog("close");
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
                pedido.dialog("close");
            }
        });
    }
}
