-- Function: tabla_moto(integer, text, text, integer, integer)

-- DROP FUNCTION tabla_moto(integer, text, text, integer, integer);

CREATE OR REPLACE FUNCTION tabla_moto(id_des integer, search_ text, order_ text, start_ integer, length_ integer)
  RETURNS text AS
$BODY$
declare
	l json;
	t integer;
	id_emp integer;
begin
	select count(id) from motorizado_moto where estado=true into t;
	select empresa_id from usuario_empleado where usuario_ptr_id = id_des limit 1 into id_emp;
	if id_emp is null then
		id_emp:=0;
	end if;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		  select m.placa,m.tipo,m.marca,m.t_propiedad,s."numeroS",t."numeroT",m.id from motorizado_moto as m inner join motorizado_soat as s on (m.soat_id=s.id and m.estado=true and m."empresaM_id"=id_emp) inner join motorizado_tecno as t on(t.id=m.tecno_id) where
		  m.placa like '%'||search_||'%' or m.tipo like '%'||search_||'%' or m.marca like '%'||search_||'%' or m.t_propiedad like '%'||search_||'%' or t."numeroT" like '%'||search_||'%' or s."numeroS" like '%'||search_||'%' limit length_ offset start_
	) p into l;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION tabla_moto(integer, text, text, integer, integer)
  OWNER TO postgres;
