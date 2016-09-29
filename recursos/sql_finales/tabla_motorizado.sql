-- Function: tabla_motorizado(integer, text, text, integer, integer)

-- DROP FUNCTION tabla_motorizado(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION tabla_motorizado(id_des integer, search_ text, order_ text, start_ integer, length_ integer)
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
	if length(search_) = 0 then
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select u.tipo_id||'-'||u.identificacion as ident,a.first_name as nom,a.last_name as ape,m.placa,mz.identifier as gps,m.id as id_mot,mz.id as id_emp from motorizado_motorizado as mz
			inner join usuario_empleado as e on(mz.empleado_id=e.usuario_ptr_id and e.empresa_id=id_emp)
			inner join motorizado_moto as m on (mz.moto_id=m.id and m.estado=true)
			inner join auth_user as a on (a.id=e.usuario_ptr_id)
			inner join usuario_usuario as u on (u.user_ptr_id = e.usuario_ptr_id)
		) p into l;
	else
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select u.tipo_id||'-'||u.identificacion as ident,a.first_name as nom,a.last_name as ape,m.placa,mz.identifier as gps,m.id as id_mot,mz.id as id_emp from motorizado_motorizado as mz
			inner join usuario_empleado as e on(mz.empleado_id=e.usuario_ptr_id and e.empresa_id=id_emp)
			inner join motorizado_moto as m on (mz.moto_id=m.id)
			inner join auth_user as a on (a.id=e.usuario_ptr_id)
			inner join usuario_usuario as u on (u.user_ptr_id = e.usuario_ptr_id) where
			u.identificacion like '%'||search_||'%' or a.first_name like '%'||search_||'%' or a.last_name like '%'||search_||'%' or m.placa like '%'||search_||'%' or mz.identifier like '%'||search_||'%' limit length_ offset start_
		) p into l;
	end if;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION tabla_motorizado(integer, text, text, integer, integer)
  OWNER TO postgres;
