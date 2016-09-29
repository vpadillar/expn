$(function(){
	$('#search').keyup(function(){
		window.table.column(1).search($(this).val()).draw();
		/*$.ajax({
			type : "POST",
			url : "/plataforma/users/cliente/search/results/",
			data : {
				'search_text' : $('#search').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success : searchSuccess,
			dataType: 'html'
		});*/
	});
});
/*
function searchSuccess(data,textStatus,jqXHR){
	$('#search-results').html(data);
}
*/
