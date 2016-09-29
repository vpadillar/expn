-- Function: tabla_tienda(integer, text, integer, integer)

-- DROP FUNCTION tabla_tienda(integer, text, integer, integer);

CREATE OR REPLACE FUNCTION tabla_tienda(id_user integer, search_ text, start_ integer, length_ integer)
  RETURNS text AS
$BODY$
declare
	l json;
	t integer;
	id_emp integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id = id_user limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select count(id) from usuario_tienda where status=true and empresa_id = id_emp into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		  select t.nit,c.nombre as ciudad,t.nombre,t.direccion,case when t.fijo is not null and length(t.fijo) <> 0 then t.fijo else 'No Registrado' end as fijo,case when t.celular is not null and length(t.celular) <> 0 then t.celular else 'No Registrado' end as celular,t.id
			from usuario_tienda as t inner join usuario_ciudad as c on(t.ciudad_id = c.id and c.status=true and t.status =true and t.empresa_id=1)where
		  t.nit like '%'||search_||'%' or c.nombre like '%'||search_||'%' or t.nombre like '%'||search_||'%' or t.direccion like '%'||search_||'%' or t.fijo like '%'||search_||'%' or t.celular like '%'||search_||'%' limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION tabla_tienda(integer, text, integer, integer)
  OWNER TO postgres;
