-- Function: tabla_pedidos_motorizado(integer, text, text, integer, integer)

-- DROP FUNCTION tabla_pedidos_motorizado(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION tabla_pedidos_motorizado(id_des integer, search_ text, order_ text, start_ integer, length_ integer)
  RETURNS text AS
$BODY$
declare
	l json;
	t integer :=0;
	id_emp integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select count(empresa_id) from pedido_pedido where motorizado_id = id_des  into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select num_pedido as num,npedido_express as exp,tablameses(fecha_pedido) as fecha, id,case when entregado then 1 else 0 end as foto,case when entregado then 1 else 0 end as entra
		from pedido_pedido where motorizado_id=id_des and (num_pedido like '%'||search_||'%' or npedido_express like '%'||search_||'%') order by fecha_pedido desc,entregado limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION tabla_pedidos_motorizado(integer, text, text, integer, integer)
  OWNER TO postgres;
