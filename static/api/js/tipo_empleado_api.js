var men;
$(document).ready(function(){
	var b = new Browser();
	if(b.name != "chrome"){
		$('#inicio, input[type="date"]').datepick();
	}
	$('#id_busq').on('click',function(){
		var ini =$('#inicio'),fin = $('#fin');
		var res= true;
		if (ini.val() .length > 0 && fin.val().length>0){
			if(ini.val() < fin.val()){
				actualizarTablaInfo();
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
		}
		actualizarTablaInfo();
	});
	men=$("#men").dialog({
        autoOpen: false,
        draggable: false,
        modal:true,
        show: {
            effect: "drop",
            direction:"up",
            duration: 500
        },
        hide: {
            effect: "drop",
            direction:"up",
            duration: 500
        },
        buttons: {
        	"Ok":function(){
            	$(this).dialog("close");
            }
        }
    });
});

function actualizarTablaInfo(){
	window.table.destroy();
	//window.table.draw();
	tablaPedidos();
}