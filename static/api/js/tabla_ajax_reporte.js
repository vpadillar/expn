function tablaReporte(){
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
            "url": "/plataforma/motorizado/search/reporte/",
            'data':{ini:$('#inicio').val(),fin:$('#fin').val(),ciu:$('#id_ciudad').val()}

        },
        "drawCallback": function (row, data) {
           	//funciones a cargar luego de el llamado
        },
        "columns": [
            {
                "data": "nump"
            },
            {
                "data": "cliente"
            },
            {
            	"data":"supervisor"
            },
            {
            	"data":"alistador"
            },
            {
            	"data":"motori"
            },
            {
            	"data":"total"
            },
            {
                "data": "alistar"
            },
            {
                "data": "despacho"
            },
            {
                "data": "entrega"
            }
        ]
    });
}
function hides(){
	$('#search-results_filter,#dataTables_length').hide();
}
tablaReporte();
init();
//window.onload = hides;