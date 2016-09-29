-- Function: tabla_info_empleado_actualizado(integer, text, text, integer, integer, text, text, integer)

-- DROP FUNCTION tabla_info_empleado_actualizado(integer, text, text, integer, integer, text, text, integer);

CREATE OR REPLACE FUNCTION tabla_info_empleado_actualizado(id_des integer, search_ text, order_ text, start_ integer, length_ integer, id_ciudad text, tipo_empleado text, id_tienda integer)
  RETURNS text AS
$BODY$
declare
	l json;
	t integer;
	id_emp integer :=0;
	tipo_emp text[] :='{"ADMINISTRADOR","SUPERVISOR","ALISTADOR","MOTORIZADO"}';
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp=0;
	end if;
	if length(tipo_empleado) > 0 then
	     tipo_emp:='{"'||tipo_empleado||'"}';
	end if;
	select count(usuario_ptr_id) from usuario_empleado where empresa_id=id_emp into t;
	if length(id_ciudad) > 0 then
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select e.cargo,u.first_name||' '||u.last_name as nom, e.usuario_ptr_id as id
			from usuario_empleado as e
			inner join auth_user as u on (e.usuario_ptr_id=u.id and u.is_active and e.empresa_id=id_emp and e.ciudad_id=cast(id_ciudad as integer)
				and (e.tienda_id in (select id from usuario_tienda as tien where tien.empresa_id=case when id_tienda = 0 then id_emp else id_tienda end) or e.tienda_id=case when id_tienda!=0 then id_tienda else 0 end ))
				  where e.cargo = any(tipo_emp::text[])  limit length_ offset start_
		) p into l;
	else
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select e.cargo,u.first_name||' '||u.last_name as nom, e.usuario_ptr_id as id
			from usuario_empleado as e
			inner join auth_user as u on (e.usuario_ptr_id=u.id and u.is_active and e.empresa_id=id_emp
				and (e.tienda_id in (select id from usuario_tienda as tien where tien.empresa_id=case when id_tienda = 0 then id_emp else id_tienda end) or e.tienda_id=case when id_tienda!=0 then id_tienda else 0 end ) )
				  where e.cargo = any(tipo_emp::text[]) limit length_ offset start_
		) p into l;
	end if;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION tabla_info_empleado_actualizado(integer, text, text, integer, integer, text, text, integer)
  OWNER TO postgres;
