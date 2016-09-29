function tablaMotorizadoPedidos(){
			window.table = $('#search-results').DataTable({
		        "bPaginate": true,
		        "bScrollCollapse": true,
		        "sPaginationType": "full_numbers",
		        "bRetrieve": true,
		        "oLanguage": {
		            "sProcessing": "Procesando...",
		            "sLengthMenu": "Mostrar _MENU_ Registros",
		            "sZeroRecords": "No hay pedidos que asignar.",
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
		            "url": "/pedidos/asignar/motorizado/search/"

		        },
		        "drawCallback": function (row, data) {

		        },
		        "columns": [
		            {
		                "data": "num"
		            },
		            {
		                "data": "nom",
		            },
		            {
		                "data": "fecha",
		                "render": function ( data, type, full, meta ) {
		                	var m="";
		                	m="<a href=\"/pedidos/asignar/motorizado/pedido/"+full.id+"/\" class=\"ui icon blue small button\">Asignar</a>";
		                	return m;

										}
		            }
		        ]
		    });
		}
		function hides(){
			$('#search-results_filter,#dataTables_length').hide();
		}
		tablaMotorizadoPedidos();
		init();
		//window.onload = hides;
