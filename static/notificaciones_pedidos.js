var elem = new Array();
$(document).on('ready',function(){
  $('body').bind('DOMNodeInserted', function(e) {
      var element = e.target;
      console.log(element.nodeName);
      if(element.nodeName == 'ARTICLE'){
        $(''+element.nodeName+'').addClass('noty');
        cambiarFondoNotificacion();
      }
    });
    $.ajax({
      url:'/plataforma/pedido/ws/notificaciones/',
      type:'post',
      dataType:'json',
      success:function(data){
          console.log(data);
          for(var i=0;data.length;i++){
            var id2=data[i].id;
            var ape=data[i].apellido;
            var dir=data[i].dir,
            emp=data[i].emp,
            emp_dir=data[i].emp_dir,
            nom=data[i].nom;
            var men ="Cliente : "+nom+" "+ape+"<br>Dirección : "+dir+"<br>Empresa Dirección : "+emp_dir;
            men+="<input type=\"radio\" style=\"visibility:hidden;\" value=\""+id2+"\" name=\"id_ped\">";
            //alertify.success("Visita nuestro <a href=\"http://blog.reaccionestudio.com/\" style=\"color:white;\" target=\"_blank\"><b>BLOG.</b></a>");
            elem.push({"id":id2,"c":alertify.success(men)});
          }
          cambiarFondoNotificacion();
      }
    });

});

function cambiarFondoNotificacion(){

  $('article.alertify-log.alertify-log-success.alertify-log-show').on('click',function(){
    aler("click");
    $(this).addClass('fondo_noti');
  });
  $('.noty').on('click',function(){
    $('.noty').removeClass('fondo_noti');
    $(this).addClass('fondo_noti');
    $('input[name="id_ped"]:checked').prop('checked',false);
    $(this).find('input[name="id_ped"][type="radio"]').prop('checked',true);
    return;
  });
}
