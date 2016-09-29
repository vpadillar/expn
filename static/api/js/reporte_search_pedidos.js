$(function(){
	$('#search').keyup(function(){
		window.table.column(1).search($(this).val()).draw();
	});
});