-- Function: aceptar_pw_service(integer, text)

-- DROP FUNCTION aceptar_pw_service(integer, text);
select * from pedido_pedidow  select * from usuario_cliente
select replace(t.direccion,'"','') from (select  id,(cast(cliente as json)::json->'direccion')::text as direccion from pedido_pedidows where motorizado_id=8 
union 
select p.id, replace(t.direccion,'"','') as direccion from pedido_pedido as p inner join usuario_cliente as c on(p.cliente_id=c.id and c.id=1 and p.motorizado_id=8)) as t

select (
select COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select replace(t.direccion,'"','') as direccion from (select  id,(cast(cliente as json)::json->'direccion')::text as direccion from pedido_pedidows where motorizado_id=m.empleado_id 
		union 
		select p.id, c.direccion as direccion from pedido_pedido as p inner join usuario_cliente as c on(p.cliente_id=c.id and c.id=1 and p.motorizado_id=m.empleado_id)) as t
	) p
) as pepidos  from motorizado_motorizado as m where m.empleado_id=8 limit 1
select * from motorizado_motorizado
select cliente  from pedido_pedidows where motorizado_id=8 
update pedido_pedidows set cliente = regexp_replace(cliente,'dirreccion','direccion')

select aceptar_pw_service(111,'359291054481645')
SELECT regexp_replace('Cat bobcat cat cats catfish', 'cat', 'dog');

select cast(cliente as json)::json->direccion from pedido_pedidows where motorizado_id=8 
select cast(cliente as json) from pedido_pedidows where motorizado_id=8 

CREATE OR REPLACE FUNCTION aceptar_pw_service(id_pedido integer, idt_motor text)
  RETURNS text AS
$BODY$
declare 
	pedido record;
	motorizado record;
begin 
	select * from pedido_pedidows as pw inner join usuario_tienda as t on(pw.tienda_id=t.id and pw.id= id_pedido) limit 1 into pedido;
	if pedido.id is not null then
		select * from motorizado_motorizado as m inner join usuario_empleado as e on (m.empleado_id=e.usuario_ptr_id and m.identifier=idt_motor and e.empresa_id=1)  limit 1 into motorizado;
		if motorizado.id is not null then
			update pedido_pedidows set motorizado_id = motorizado.usuario_ptr_id, confirmado=true where id = id_pedido;
			return '{"r":true}';
		end if;
	end if; 
	return '{"r":false}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION aceptar_pw_service(integer, text)
  OWNER TO postgres;
