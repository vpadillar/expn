$( document ).ready(function() {
  $('#id_busq').on('click',function(event){
      $.ajax({
          url:'/pedidos/ws/info/pedido/',
          type:'post',
          dataType:'json',
          data:{pedido:$('#pedido').val()},
          success:function(data){
              if(data.r){
                  var res = data.lista[0];
                  $('.clear').val("");
                  $('#creado').val(res.creado);
                  $('#alistamiento').val(res.alistamiento);
                  $('#entrega').val(res.entregado);
                  $('#cliente').val(res.cliente);
              }else{
                  $('.clear, #pedido').val("");
                  alert("El pedido no se encuentra registrado.");
              }
          }
      });
  });
});
