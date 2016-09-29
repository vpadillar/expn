-- Function: tabla_cliente(integer, text, integer, integer, integer)

-- DROP FUNCTION tabla_cliente(integer, text, integer, integer, integer);

CREATE OR REPLACE FUNCTION tabla_cliente(id_des integer, search_ text, order_ integer, start_ integer, length_ integer)
  RETURNS text AS
$BODY$
declare 
	l json;
	t integer;
begin
	select count(id) from domicilios_cliente into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		 select first_name as nom,last_name as ape,identificacion as id from usuario_cliente where 
		 first_name like '%'||search_||'%' or last_name like '%'||search_||'%' or identificacion like '%'||search_||'%' limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION tabla_cliente(integer, text, integer, integer, integer)
  OWNER TO postgres;



-- Function: tabla_cliente(integer, text, integer, integer, integer)

-- DROP FUNCTION tabla_cliente(integer, text, integer, integer, integer);

select tabla_cliente(3,'',0,0,10)
tabla_cliente

select * from usuario_cliente
CREATE OR REPLACE FUNCTION tabla_cliente(id_des integer, search_ text, order_ integer, start_ integer, length_ integer)
  RETURNS text AS
$BODY$
declare 
	l json;
	t integer;
	id_emp integer;
begin
	select empresa_id from usuario_empleado where usuario_ptr_id=id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	select count(id) from usuario_cliente where empresa_id=id_emp into t;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		 select first_name as nom,last_name as ape,identificacion as id, from usuario_cliente where empresa_id=id_emp and
		 first_name like '%'||search_||'%' or last_name like '%'||search_||'%' or identificacion like '%'||search_||'%' limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION tabla_cliente(integer, text, integer, integer, integer)
  OWNER TO postgres;


