function tablaTienda(){
			window.table = $('#search-results').DataTable({
		        "bPaginate": true,
		        "bScrollCollapse": true,
		        "sPaginationType": "full_numbers",
		        "bRetrieve": true,
		        "oLanguage": {
		            "sProcessing": "Procesando...",
		            "sLengthMenu": "Mostrar _MENU_ Registros",
		            "sZeroRecords": "No se encontraron tiendas",
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
		            "url": "/usuario/tienda/list/search/"

		        },
		        "drawCallback": function (row, data) {
		           	/*$('.stop').on('click',function(){return false;});
		           	$('.delete').on('click',function(){
									console.log($(this).attr('href'));
								});*/
		        },
		        "columns": [
		            {
		                "data": "nit"
		            },
		            {
		                "data": "ciudad"
		            },
		            {
		            	"data":"nombre"
		            },
		            {
		                "data": "direccion"
		            },
		            {
		                "data": "fijo"
		            },
		            {
		                "data": "celular"
		            },
		            {
		            	"className":"right aligned",
		                "data": "id",
		                "render": function ( data, type, full, meta ) {
		                	var m="";
		                	m="<a href=\"/usuario/tienda/details/"+data+"/\" class=\"ui icon green\"><i class=\"material-icons green\">remove_red_eye</i></a>";
		                	m+="<a href=\"/usuario/tienda/edit/"+data+"/\" class=\"ui icon green \"><i class=\"material-icons green\">mode_edit</i></a>";
		                	m+="<a id=\"eliminar\" href=\"/usuario/tienda/delete/"+data+"/\" class=\"ui icon green stop delete\"><i class=\"material-icons red\">delete_forever</i></a>";
		                	return m;
						}
		            }
		        ]
		    });
		}
		function hides(){
			$('#search-results_filter,#dataTables_length').hide();
		}
		tablaTienda();
		init();
		window.onload = hides;
