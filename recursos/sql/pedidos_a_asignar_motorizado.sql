--select pedidos_a_asignar_motor(10,0,10)

CREATE OR REPLACE FUNCTION pedidos_a_asignar_motor(id_des integer, start_ integer, length_ integer)
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
		 select p.num_pedido as num,upper(u.first_name)||' '||upper(u.last_name) as nom,tablameses(p.fecha_pedido) as fecha,p.id  
			from pedido_pedido as p inner join auth_user  as u on (p.alistador_id=id_des and p.supervisor_id=u.id and p.motorizado_id is null)
	) p into l ;
	return '{"recordsFiltered": '|| t ||', "recordsTotal": '|| json_array_length(l) ||', "data": '|| l||'}';

end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION pedidos_a_asignar_motor(integer, integer, integer)
  OWNER TO postgres;
 
 --select case when motorizado_id is null then 1 else 0 end  from pedido_pedido
 --select * from pedido_pedido
--  select * from pedido_pedido

 --select * from auth_user
 --select * from usuario_usuario
 --select p.num_pedido as num,upper(u.first_name)||' '||upper(u.last_name) as nom,tablameses(p.fecha_pedido) as fecha from pedido_pedido as p inner join auth_user  as u on (p.alistador_id=10 and p.supervisor_id=u.id and p.motorizado_id is null)



 -- Function: tablameses(date)

-- DROP FUNCTION tablameses(date);
--select tablameses('2016-06-5')

CREATE OR REPLACE FUNCTION tablameses(f date)
  RETURNS text AS
$BODY$
declare
	a text[] :='{" de Enero de "," de Febrero de "," de Marzo de "," de Abril de "," de Mayo de "," de Junio de "," de Julio de "," de Agosto de "," de Septiembre de "," de Octubre de "," de Noviembre de "," de Diciembre de "}';
begin
	return (extract(day from f)||a[extract(month from f)]||extract(year from f));
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION tablameses(date)
  OWNER TO postgres;





﻿-- Function: mis_pedidos_asignados(integer, integer, integer)

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

