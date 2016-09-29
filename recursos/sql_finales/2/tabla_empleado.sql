-- Function: tabla_empleado(integer, text, text, integer, intesearchMotorizado
-- DROP FUNCTION tabla_empleado(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION tabla_empleado(id_des integer, search_ text, order_ text, start_ integer, length_ integer)
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
	select count(usuario_ptr_id) from usuario_empleado where empresa_id=id_emp into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		  select user_.first_name as nom,user_.last_name as ape,u.identificacion as ced,e.cargo,emp.first_name,
		  case when user_.is_active then 'Activo' else 'Desactivado'end as estado,e.usuario_ptr_id  from usuario_empleado as e
		  inner join usuario_usuario as u on (e.usuario_ptr_id=u.user_ptr_id and e.empresa_id=id_emp)
		  inner join auth_user as user_ on(u.user_ptr_id=user_.id) inner join usuario_empresa as emp on (e.empresa_id=emp.id and emp.id=empresa_id) where
		  user_.first_name like '%'||search_||'%' or user_.last_name  like '%'||search_||'%' or u.identificacion like '%'||search_||'%' or e.cargo like '%'||search_||'%' or emp.first_name like '%'||search_||'%' limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE 
  COST 100;
ALTER FUNCTION tabla_empleado(integer, text, text, integer, integer)
  OWNER TO postgres;