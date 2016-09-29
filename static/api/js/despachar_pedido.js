var dialogo, pedido, men;
$(document).on('ready', function() {
    $("#modal1").show();
    dialogo = $("#modal1").dialog({
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
            "OK": envio

        }
    });
    pedido = $("#mod_pedido").dialog({
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
            "OK": entrega

        }
    });
    men = $("#men").dialog({
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

function envio() {
    var id = $('input[name="opt"]:checked').val();
    if (id != undefined) {
        $.ajax({
            url: '/pedidos/pedido/despacho/update/',
            data: {
                id_ped: id
            },
            dataType: 'json',
            type: 'post',
            success: function(response) {
                window.table.column(1).search($('#search').val()).draw();
                dialogo.dialog("close");
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
