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
            "url": "/plataforma/pedido/search/pedidos/"

        },
        "drawCallback": function (row, data) {
           	//funciones a cargar luego de el llamado
            
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
                		m="<i class=\"checkmark large green icon\"></i>";
                	}else{
                		m="<i class=\"remove large red icon\"> </i>";
                	}
                	
                	return m;
				}
            },
            {
            	"className":"center aligned",
                "data": "id",
                "render": function ( data, type, full, meta ) {
                	var m="";
                	m+="<a href=\"/plataforma/pedido/"+data+"/info/\" class=\"ui icon green\"><i class=\"unhide large green icon\"></i></a>";
                	m+="<a href=\"/plataforma/pedido/edit/"+data+"/\" class=\"ui icon green\"><i class=\"edit large green icon\"></i></a>";
                	m+="<a href=\"/plataforma/pedido/factura/"+data+"\" class=\"ui icon \"><i class=\"print large green icon\"></i></a>";
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