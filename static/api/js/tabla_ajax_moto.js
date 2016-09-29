function tablaMotorizado(){
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
		            "url": "/motorizado/moto/search/"

		        },
		        "drawCallback": function (row, data) {
		           	//funciones a cargar luego de el llamado
		        },
		        "columns": [
		            {
		                "data": "placa"
		            },
		            {
		                "data": "tipo"
		            },
		            {
		            	"data":"marca"
		            },
		            {
		                "data": "t_propiedad"
		            },
		            {
		                "data": "numeroS"
		            },
		            {
		                "data": "numeroT"
		            },
		            {
		            	"className":"left aligned",
		                "data": "id",
		                "render": function ( data, type, full, meta ) {
		                	var m="";
		                	m="<a href=\"/motorizado/moto/details/"+data+"/\" class=\"ui icon green\"><i class=\"material-icons green\">remove_red_eye</i></a>";
		                	m+="<a href=\"/motorizado/moto/edit/"+data+"/\" class=\"ui icon green \"><i class=\"material-icons green\">mode_edit</i></a>";
		                	m+="<a id=\"eliminar\" href=\"/motorizado/moto/delete/"+data+"/\" class=\"ui icon green\"><i class=\"material-icons red\">delete_forever</i></a>";
		                	return m;
						}
		            }
		        ]
		    });
		}
		function hides(){
			$('#search-results_filter,#dataTables_length').hide();
		}
		tablaMotorizado();
		init();
		window.onload = hides;
