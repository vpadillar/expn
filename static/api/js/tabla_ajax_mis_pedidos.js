function tablaMisPedidos(){
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
            "url": "/pedidos/pedido/mis/pedidos/"

        },
        "drawCallback": function (row, data) {
           	//funciones a cargar luego de el llamado

        },
        "columns": [
            {
                "data": "num"
            },
            {
            	"data":"nom"
            },
            {
            	"class":"center aligned",
                "data": "fecha",
            },
            {
            	"className":"center aligned",
                "data": "id",
                "render": function ( data, type, full, meta ) {
                	var m="";
                	m+="<a href=\"/pedidos/pedido/info/"+data+"/\" class=\"ui icon green\"><i class=\"unhide large green icon\"></i></a>";
                	return m;
				}
            }
        ]
    });
}
function hides(){
	$('#search-results_filter,#dataTables_length').hide();
}
tablaMisPedidos();
init();
window.onload = hides;
