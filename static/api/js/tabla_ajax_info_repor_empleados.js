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
            "url": "/reporte/tabla/info/empleados/",
            "data":{ciudad:$('#id_ciudad').val(),id_emp_tipo:$('#tipo').val(),
					inicio:$('#inicio').val(),fin:$('#fin').val(),tienda:$('#tienda').val(),
					estado:$('#envio:checked').val() != undefined?1:0}
        },
        "drawCallback": function (row, data) {
           	//funciones a cargar luego de el llamado
            $('.pdf,.excel').on('click',function(){
                var ini =$('#inicio'),fin = $('#fin');
                var res= true;
                if (ini.val() .length > 0 && fin.val().length>0){
                    if(ini.val() < fin.val()){
                        if($(this).hasClass('excel')){
                            window.location.href = "/reporte/excel/?id="+$(this).parent().find('input[type="hidden"]').val()+"&ini="+$('#inicio').val()+"&fin="+$('#fin').val()+"&estado="+$('#envio:checked').val();
                        }else if($(this).hasClass('pdf')){
                            window.location.href = "/reporte/pdf/?id="+$(this).parent().find('input[type="hidden"]').val()+"&ini="+$('#inicio').val()+"&fin="+$('#fin').val()+"&estado="+$('#envio:checked').val();
                        }
                    }else{
                        $('#men span').text("La fecha de fin en el intervalo debe ser mayor.");
                        fin.val("");
                        men.dialog('open');
                        return;
                    }
                }else if((ini.val() .length >0 && fin.val().length == 0) || (fin.val() .length >0 && ini.val().length == 0) ){
                    $('#men span').text("La intervalo de fecha debe ser valido.");
                    men.dialog('open');
                    return;
                }else{
                   $('#men span').text("Debe seleccionar un rango de fecha.");
                    men.dialog('open');
                    return;
                }
            });

        },
        "columns": [
            {
                "data": "cargo"
            },
            {
                "data": "nom"
            },
            {
            	"class":"center aligned",
                "data": "id",
                "render": function ( data, type, full, meta ) {
                	var m="";
                	//m="<a href=\"/plataforma/reporte/report/empleado/pdf/\" target=\"_blank\" onClick=\"window.open(this.href, this.target, 'width=300,height=400'); return false;\" class=\"pdf\" ><img src=\"/static/img/pdf24.png\"></a> " ;
                    m="<a href=\"#\" class=\"pdf\" ><img src=\"/static/img/pdf24.png\"></a> " ;
                    m+="<a href=\"#\" class=\"excel\" ><img src=\"/static/img/excel24.png\"></a> " ;
                    m+="<input type=\"hidden\" value=\""+data+"\">";
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
