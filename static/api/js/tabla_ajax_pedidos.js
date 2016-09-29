function tablaPedidos(){
	window.table = $('#search-results').DataTable({
        "bPaginate": true,
        "bScrollCollapse": true,
        "sPaginationType": "full_numbers",
        "bRetrieve": true,
        "oLanguage": {
            "sProcessing": "Procesando...",
            "sLengthMenu": "Mostrar _MENU_ Registros",
            "sZeroRecords": "No se encontraron resultados",
            "sInfo": "Mostrando desde _START_ hasta _END_ de _TOTAL_ Registros",
            "sInfoEmpty": "Mostrando desde 0 hasta 0 de 0 Registros",
            "sInfoFiltered": "(filtrado de _MAX_ registros en total)",
            "sInfoPostFix": "",
            "sSearch": "Buscar:",
            "sUrl": "",
            "oPaginate": {
                "sFirst": "|<<",
                "sPrevious": "<<",
                "sNext": ">>",
                "sLast": ">>|"
            }
        },
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/pedidos/pedido/search/"

        },
        "drawCallback": function (row, data) {
           	//funciones a cargar luego de el llamado
			$('.stop').on('click',function(even){
				return false;
			});
			$('.imp').on('click',function(even){
				var win = window.open($(this).attr('href'), '_blank');
					win.focus();
			});
			$('.desactivar').on('click',function(even){
				var res_act = $(this).parents('tr').find('input[type="hidden"][name="estado"]').val();
				console.log(res_act);
				$(this).parent().find('input[type="radio"]').prop('checked',true);
				if (res_act == "0"){
					$('#cancelar').text("Esta seguro de cancelar el pedido "+$(this).parents('tr').find('td:first').text());
					cancelar.dialog('open');
				}else{
					$('#men').text("Este pedido "+$(this).parents('tr').find('td:first').text()+" fue entregado.");
					mensaje.dialog('open');
				}
			});
			$('.activar').on('click',function(even){
				$('#activar').text('Desea reactivar el pedido '+$(this).parents('tr').find('td:first').text());
				$(this).parent().find('input[type="radio"]').prop('checked',true);
				activar.dialog('open');
			});
        },
        "columns": [
            {
                "data": "num"
            },
            {
                "data": "emp"
            },
            {
            	"data":"sup"
            },
            {
            	"data":"alis"
            },
            {
            	"data":"moto"
            },
            {
            	"data":"total"
            },
            {
            	"class":"center aligned",
                "data": "estado",
                "render": function ( data, type, full, meta ) {
                	var m="";
                	if (data == 1){
                		m="<i class=\"material-icons green\">done</i>";
                	}else{
                		m="<i class=\"material-icons red\">clear</i>";
                	}
					m+="<input type=\"hidden\" name=\"estado\" value=\""+data+"\">" ;
                	return m;
				}
            },
            {
            	"class":"center aligned",
                "data": "activado",
                "render": function ( data, type, full, meta ) {
                	var m="";
					if (full.activacion==0){
	                	if (data == 1){
	                		m="<i class=\"material-icons desactivar green\">done</i>";
	                	}else{
	                		m="<i class=\"material-icons red activar\">clear</i>";
	                	}
						m+="<input type=\"hidden\" name=\"activado\" value=\""+data+"\">";
						m+="<input style=\"visibility: hidden;\" type=\"radio\" name=\"pedido\" value=\""+full.id+"\">";
					}
                	return m;
				}
            },
            {
            	"className":"center aligned",
                "data": "id",
                "render": function ( data, type, full, meta ) {
                	var m="";
                	m+="<a href=\"/pedidos/pedido/info/"+data+"/\" class=\"ui icon green\"><i class=\"material-icons green\">remove_red_eye</i></a>";
					if (full.estado == 0 && full.activacion==0){
                		m+="<a href=\"/pedidos/pedido/edit/"+data+"/\" class=\"ui icon green\"><i class=\"material-icons green\">mode_edit</i></a>";
					}
                	m+="<a href=\"/pedidos/pedido/factura/"+data+"\" class=\"ui icon stop imp\"><i class=\"material-icons green\">print</i></a>";
                	return m;
				}
            }
        ]
    });
}
function hides(){
	$('#search-results_filter,#dataTables_length').hide();
}
tablaPedidos();
init();
window.onload = hides;
