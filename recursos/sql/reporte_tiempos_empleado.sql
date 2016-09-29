-- Function: reporte_tiempos_empleados(integer, text, text, integer, integer, integer)

-- DROP FUNCTION reporte_tiempos_empleados(integer, text, text, integer, integer, integer);

CREATE OR REPLACE FUNCTION reporte_tiempos_empleados(id_des integer, search_ text, order_ text, start_ integer, length_ integer, id_user_sec integer)
  RETURNS text AS
$BODY$
declare 
	l json;
	t integer :=0;
	id_emp integer;
	typo integer ;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select case when cargo='ADMINISTRADOR' then 1 when cargo='SUPERVISOR' then 2 when cargo='ALISTADOR' then 3 else 4 end as peso 
	from usuario_empleado where usuario_ptr_id=id_des limit 1 into typo;
	if typo is null then
		typo=0;
		id_des:=0;
	end if;
	
	if typo=1 then
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select nump,cliente,supervisor,alistador,motori,alistar,despacho,entrega from pedidos_tiempos where empresa_id=id_emp order by fecha desc
			limit length_ offset start_
		) p into l; 
	elsif typo=2 then 
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select nump,cliente,supervisor,alistador,motori,alistar,despacho,entrega from pedidos_tiempos where supervisor_id=id_des and  empresa_id=id_emp  order by fecha desc
			limit length_ offset start_
		) p into l; 
	elsif typo=3 then
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select nump,cliente,supervisor,alistador,motori,alistar,despacho,entrega from pedidos_tiempos where alistador_id=id_des and  empresa_id=id_emp   order by fecha desc
			limit length_ offset start_
		) p into l; 
	else
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select nump,cliente,supervisor,alistador,motori,alistar,despacho,entrega from pedidos_tiempos where motorizado_id=id_des and  empresa_id=id_emp   order by fecha desc
			limit length_ offset start_
		) p into l; 
	end if;
	select count(empresa_id) from pedido_pedido where empresa_id = id_emp  into t;			  
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION reporte_tiempos_empleados(integer, text, text, integer, integer, integer)
  OWNER TO postgres;

select * from pedidos_tiempos