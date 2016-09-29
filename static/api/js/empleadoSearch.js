$(function(){
	$('#search').keyup(function(){
		window.table.column(1).search($(this).val()).draw();
	});
});

function searchSuccess(data,textStatus,jqXHR){
	$('#search-results').html(data);
}
