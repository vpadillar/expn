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
            "url": "/pedidos/pedido/despacho/search/"

        },
        "drawCallback": function (row, data) {
           	//funciones a cargar luego de el llamado
            $('.accion').on('click',function(){
                $(this).parent().find('input[type="radio"]').prop('checked',true);
                var c =$(this).parents('tr');
                $('.cont').text($(this).parent().find('input[name="estado"]').val()==0?"Esta seguro de asignar el pedido "+c.find('input[name="pedido"]').val()+" a el motorizado "+c.find('input[name="moto"]').val()+"?":"Esta seguro de desasignar el pedido "+c.find('input[name="pedido"]').val()+" a el motorizado "+c.find('input[name="moto"]').val()+"?");
                dialogo.dialog("open");
            });
            $('.entrega').on('click',function(){
                $(this).parent().find('input[type="radio"]').prop('checked',true);
                var c =$(this).parents('tr');
                if(c.find('input[name="estado"]').val()==0){
                    $('.cont2').text("El pedido debe ser entregado.");
                    men.dialog("open");
                    return;
                }
                $('.conte').text($(this).parent().find('input[name="estadod"]').val()==0?"Esta seguro de que el pedido "+c.find('input[name="pedido"]').val()+" fue entregado por el motorizado "+c.find('input[name="moto"]').val()+"?":"Esta seguro de cancelar la entrega del pedido "+c.find('input[name="pedido"]').val()+" por el motorizado "+c.find('input[name="moto"]').val()+"?");
                pedido.dialog("open");
            });
        },
        "columns": [
            {
                "data": "num",
                "render":function(data, type, full, meta ){
                    var m="";
                    m+="<span>"+data+"</span>";
                    m+="<input name=\"pedido\" type=\"hidden\" value=\""+data+"\">";
                    return m;
                }
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
            	"data":"moto",
                "render":function(data, type, full, meta ){
                    var m="";
                    m+="<span>"+data+"</span>";
                    m+="<input name=\"moto\" type=\"hidden\" value=\""+data+"\">";
                    return m;
                }
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
                		m="<a class=\"accion\" href=\"#\"><i class=\"checkmark large green icon\"></i></a>";
                	}else{
                		m="<a class=\"accion\" href=\"#\"><i class=\"remove large red icon\"> </i></a>";
                	}
                	m+="<input name=\"estado\" type=\"hidden\" value=\""+data+"\">";
                    m+="<input type=\"radio\" name=\"opt\" style=\"visibility: hidden;\" value=\""+full.id+"\">";
                	return m;
				}
            },
            {
                "class":"center aligned",
                "data": "entregado",
                "render": function ( data, type, full, meta ) {
                    var m="";
                    if (data == 1){
                        m="<a class=\"entrega\" href=\"#\"><i class=\"checkmark large green icon\"></i></a>";
                    }else{
                        m="<a class=\"entrega\" href=\"#\"><i class=\"remove large red icon\"> </i></a>";
                    }
                    m+="<input name=\"estadod\" type=\"hidden\" value=\""+data+"\">";
                    m+="<input type=\"radio\" name=\"ent\" style=\"visibility: hidden;\" value=\""+full.id+"\">";
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
