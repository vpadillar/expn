-- Function: reporte_pedidos(integer, text, text, integer, integer)

-- DROP FUNCTION reporte_pedidos(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION reporte_pedidos(id_des integer, search_ text, order_ text, start_ integer, length_ integer)
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

		select * from (
				select nump,express,cliente,supervisor,alistador,motori,total,
				case when alistamiento is not null then round(alistamiento::numeric,2)::text else 'No asignado' end::text as alistar,
				case when despacho is not null then round(despacho::numeric,2)::text else 'No asignado' end::text as despacho ,
				case when entrega is not null then round(entrega::numeric,2)::text else 'No asignado' end::text as entrega 
				from (
					select p.id,p.num_pedido as nump,p.npedido_express as express,c.first_name||' '||c.last_name as cliente,s.first_name||' '||s.last_name as supervisor,
					       a.first_name||' '||a.last_name as alistador,m.first_name||' '||m.last_name as motori,
					       case when p.total is not null then p.total else 0 end::text as total,
					       (EXTRACT(EPOCH from t.confirmado)-EXTRACT(EPOCH from t.creado)) /60 as alistamiento,
					       (EXTRACT(EPOCH from t.despachado)-EXTRACT(EPOCH from t.confirmado)) /60 as despacho,
					       (EXTRACT(EPOCH from t.entregado)-EXTRACT(EPOCH from t.despachado)) /60 as entrega
							from pedido_pedido as p inner join auth_user as m on(p.motorizado_id=m.id)  
							inner join auth_user as a on (p.alistador_id=a.id) inner join auth_user as s on (p.supervisor_id=s.id)
							inner join usuario_cliente as c on (p.cliente_id=c.id) inner join pedido_time as t on (p.id=t.pedido_id) 
							inner join pedido_time as ti on(ti.pedido_id=p.id) where p.empresa_id=id_emp order by p.fecha_pedido desc) as p
				    ) as pf where pf.nump like '%'||search_||'%' or pf.cliente like '%'||search_||'%' or pf.supervisor like '%'||search_||'%' or pf.alistador like '%'||search_||'%'  or pf.motori like '%'||search_||'%' limit length_ offset start_
	) p into l; 				  
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION reporte_pedidos(integer, text, text, integer, integer)
  OWNER TO postgres;
