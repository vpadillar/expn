var pedido,men,foto;
$(document).on('ready',function(){
  $("#modal1").show();
    pedido=$("#mod_pedido").dialog({
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
            "Cancelar":function(){
                $(this).dialog("close");
              },
              "OK":entrega

          }
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
    foto=$("#foto").dialog({
          autoOpen: false,
          draggable: false,
          width: 950,
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
function envio(){
  var id = $('input[name="opt"]:checked').val();
  if (id != undefined) {
    $.ajax({
              url:'/pedidos/motorizado/up/ser/pedido/',
              data:{id_ped:id},
              dataType:'json',
              type:'post',
              success:function(response){
                window.table.column(1).search($('#search').val()).draw();
                  dialogo.dialog("close");
              }
          });
  }
}
function entrega(){
  var id = $('input[name="ent"]:checked').val();
  if(id != undefined){
    $.ajax({
              url:'/pedidos/motorizado/up/ser/entrega/',
              data:{id_ped:id},
              dataType:'json',
              type:'post',
              success:function(response){
                window.table.column(1).search('').draw();
                  pedido.dialog("close");
              }
          });
  }
}
