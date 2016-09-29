function tablaMotorizadoPedidos(){
			window.table = $('#search-results').DataTable({
		        "bPaginate": true,
		        "bScrollCollapse": true,
		        "sPaginationType": "full_numbers",
		        "bRetrieve": true,
		        "oLanguage": {
		            "sProcessing": "Procesando...",
		            "sLengthMenu": "Mostrar _MENU_ Registros",
		            "sZeroRecords": "No tiene pedidos asignados.",
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
		            "url": "/motorizado/motorizado/search/pedido/"

		        },
		        "drawCallback": function (row, data) {
		           	$('.entrega').on('click',function(){
		                $(this).parent().find('input[type="radio"]').prop('checked',true);
		                var c =$(this).parents('tr');
		                $('.conte').text($(this).parent().find('input[name="estado"]').val()==0?"El pedido "+c.find('input[name="pedido"]').val()+" entregado.":"Esta seguro de cancelar la entrega del pedido "+c.find('input[name="pedido"]').val()+".");
		                pedido.dialog("open");
		            });
		            $('.capfoto').on('click',function(){
		            	//foto.dialog('open');
		            	$('#fot').load("/motorizado/motorizado/foto/",function(){
		            		var streaming = false,
							      video        = document.querySelector('#video'),
							      cover        = document.querySelector('#cover'),
							      canvas       = document.querySelector('#canvas'),
							      photo        = document.querySelector('#photo'),
							      startbutton  = document.querySelector('#startbutton'),
							      width = 320,
							      height = 0;

						  navigator.getMedia = ( navigator.getUserMedia ||
						                         navigator.webkitGetUserMedia ||
						                         navigator.mozGetUserMedia ||
						                         navigator.msGetUserMedia);

						  navigator.getMedia(
						    {
						      video: true,
						      audio: false
						    },
						    function(stream) {
						      if (navigator.mozGetUserMedia) {
						        video.mozSrcObject = stream;
						      } else {
						        var vendorURL = window.URL || window.webkitURL;
						        video.src = vendorURL.createObjectURL(stream);
						      }
						      video.play();
						    },
						    function(err) {
						      console.log("An error occured! " + err);
						    }
						  );

						  video.addEventListener('canplay', function(ev){
						    if (!streaming) {
						      height = video.videoHeight / (video.videoWidth/width);
						      video.setAttribute('width', width);
						      video.setAttribute('height', height);
						      canvas.setAttribute('width', width);
						      canvas.setAttribute('height', height);
						      streaming = true;
						    }
						  }, false);

						  function takepicture() {
						    canvas.width = width;
						    canvas.height = height;
						    canvas.getContext('2d').drawImage(video, 0, 0, width, height);
						    var data = canvas.toDataURL('image/png');
						    photo.setAttribute('src', data);
						  }

						  startbutton.addEventListener('click', function(ev){
						  	takepicture();
						    ev.preventDefault();
						  }, false);
		            		foto.dialog("open");
		            	});
		            });
		        },
		        "columns": [
		            {
		                "data": "num"
		            },
		            {
		                "data": "exp",
		                "render":function(data, type, full, meta ){
		                    var m="";
		                    m+="<span>"+data+"</span>";
		                    m+="<input name=\"pedido\" type=\"hidden\" value=\""+data+"\">";
		                    return m;
		                }
		            },
		            {
		            	"data":"fecha"
		            },
		            {

		                "data": "id",
		                "render": function ( data, type, full, meta ) {
		                	var m="";
		                	m="<a href=\"/pedidos/pedido/info/"+data+"/\" class=\"ui icon green\"><i class=\"unhide large green icon\"></i></a>";
		                	return m;

						}
		            },
		            {
		                "data": "foto",
		                "render": function ( data, type, full, meta ) {
		                	var m="";
		                	if (data == 1){
		                		m="<i class=\"checkmark large green icon\"></i>";
		                	}else{
		                		m="<i class=\"remove large red icon\"> </i>";
		                	}
		                	m+="<input name=\"estfot\" type=\"hidden\" value=\""+data+"\">";
		                	m+="<a href=\"#\" class=\"capfoto\"><i class=\"photo icon\"></i></a>";
		                	return m;
						}
		            },
		            {
		            	"className":"left aligned",
		                "data": "entra",
		                "render": function ( data, type, full, meta ) {
		                	var m="";
		                	if (data == 1){
		                		m="<a href=\"#\" class=\"\"><i class=\"checkmark large green icon\"></a></i>";
		                	}else{
		                		m="<a href=\"#\" class=\"entrega\"><i class=\"remove large red icon\"> </a></i>";
		                	}
		                	m+="<input name=\"estado\" type=\"hidden\" value=\""+data+"\">";
                    		m+="<input type=\"radio\" name=\"ent\" style=\"visibility: hidden;\" value=\""+full.id+"\">";
		                	return m;
						}
		            }
		        ]
		    });
		}
		function hides(){
			$('#search-results_filter,#dataTables_length').hide();
		}
		tablaMotorizadoPedidos();
		init();
		//window.onload = hides;
