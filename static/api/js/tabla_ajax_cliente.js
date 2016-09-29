function tablaClientes(){
			window.table = $('#search-results').DataTable({
		        "bPaginate": true,
		        //"bFilter": false,
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
		            "url": "/usuario/cliente/search/"

		        },
		        "drawCallback": function (row, data) {
		           	//funciones a cargar luego de el llamado
		        },
		        "columns": [
		            {
		                "data": "nom",
		            },
		            {
		                "data": "ape"
		            },
		            {
		                "data": "id"
		            },
		            {
						"data": "id2",
						"render": function ( data, type, full, meta ) {
		                    var m="";
		                    m+="<a href=\"/usuario/cliente/details/"+data+"/\" class=\"ui icon green \"><i class=\"material-icons green\">remove_red_eye</i></a>";
		                    m+="<a href=\"/usuario/cliente/edit/"+data+"/\" class=\"ui icon green \"><i class=\"material-icons green\">mode_edit</i></a>";
		                    return m;
		                }
		            }
		        ]
		    });

		}
		function hides(){
			$('#search-results_filter,#dataTables_length').hide();
		}
		tablaClientes();
		init();
		window.onload = hides;
