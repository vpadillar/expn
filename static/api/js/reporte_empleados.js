$(document).on('ready',function(){
	//$("#"+$('#acordeon > h3:first').find('label').attr('for')).find('input[type="radio"]').prop('checked',true);
	actualizarTabla($("#"+$('#acordeon > h3:first').find('label').attr('for')));
	$('#acordeon > h3').on('click',function(){
		var contenedor = $("#"+$(this).find('label').attr('for'));
		//contenedor.parent('div').find('input[type="radio"]').prop('checked',true);
		//contenedor.load("/plataforma/reporte/servi/tabla/empleado/",function(){});
		//alert($(this).find('label').attr('for'));
		actualizarTabla($("#"+$(this).find('label').attr('for')));
	});
});

function actualizarTabla(c){
	c.find('input[type="radio"]').prop('checked',true);
	$('.com_emp div').html("");
	c.find('div').load("/reporte/load/empleados/",function(){
		include(c.attr('id'),"/static/api/js/tabla_load_ajax_reporte_empleados.js");
	});
}

function include(name,archivo) {
	var nuevo = document.createElement('script');
	nuevo.setAttribute('type', 'text/javascript');
	nuevo.setAttribute('src', archivo);
	document.getElementsByTagName('head')[0].appendChild(nuevo);
}
