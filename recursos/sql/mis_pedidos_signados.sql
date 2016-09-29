-- Function: mis_pedidos_asignados(integer, integer, integer)

-- DROP FUNCTION mis_pedidos_asignados(integer, integer, integer);

CREATE OR REPLACE FUNCTION mis_pedidos_asignados(id_des integer, start_ integer, length_ integer)
  RETURNS text AS
$BODY$
declare 
	l json;
	t integer;
begin
	select count(id) from pedido_pedido where empresa_id = (select empresa_id from usuario_empleado where usuario_ptr_id=id_des limit 1) into t;
	if t is null then 
		t:=0;
	end if;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		 select distinct p.id,p.num_pedido as num,p.npedido_express as nom,tablameses(p.fecha_pedido) as fecha
		  from usuario_empleado as e 
		  inner join pedido_pedido as p 
		  on (p.supervisor_id=e.usuario_ptr_id or p.alistador_id = e.usuario_ptr_id and e.usuario_ptr_id=id_des) order by p.id desc  limit length_ offset start_
	) p into l ;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';

end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION mis_pedidos_asignados(integer, integer, integer)
  OWNER TO postgres;

 --select * from pedido_pedido
