-- Function: tabla_pedidos_despacho(integer, text, text, integer, integer)

-- DROP FUNCTION tabla_pedidos_despacho(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION tabla_pedidos_despacho(id_des integer, search_ text, order_ text, start_ integer, length_ integer)
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
	select count(empresa_id) from pedido_pedido where empresa_id = id_emp  into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select p.num_pedido as num,emp.first_name as emp,a3.first_name||' '||a3.last_name as sup,u1.first_name||' '||u1.last_name as alis,
		u2.first_name||' '||u2.last_name as moto,case when p.total is not null then to_char(p.total,'$999,999,999.9') else to_char(0,'$999,999,999.9') end as total,
		case when p.despachado then 1 else 0 end as estado,case when p.entregado then 1 else 0 end as entregado,p.id from pedido_pedido as p 
		inner join usuario_empleado as e1 on (p.alistador_id=e1.usuario_ptr_id and p.empresa_id=id_emp) 
		inner join usuario_empleado as e2 on (p.motorizado_id=e2.usuario_ptr_id) inner join auth_user as u1 on (e1.usuario_ptr_id=u1.id) 
		inner join auth_user as u2 on (e2.usuario_ptr_id=u2.id)
		inner join usuario_empresa as emp on (p.empresa_id=emp.id) inner join auth_user as a3 on (p.supervisor_id=a3.id) where 
		emp.first_name like '%'||search_||'%' or a3.first_name like '%'||search_||'%' or a3.last_name like '%'||search_||'%' or u1.first_name like '%'||search_||'%' 
		or u1.last_name like '%'||search_||'%' or u2.first_name like '%'||search_||'%' or u2.last_name like '%'||search_||'%'  limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION tabla_pedidos_despacho(integer, text, text, integer, integer)
  OWNER TO postgres;
