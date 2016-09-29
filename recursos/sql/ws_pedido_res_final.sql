select ws_add_pedido_service('{"pedido":{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"3"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},"pedido":{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}}')

select ws_add_pedido_service('{"pedido":[{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"3"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}]}')
select get_add_pedido_admin(11)
select * from pedido_configuraciontiempo
create or replace function get_add_pedido_admin(id_pedido integer) returns json as $$
declare 
begin
	return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select id, motorizado_id as motorizado,10000*(select retraso from pedido_configuraciontiempo order by id desc limit 1) as retraso,
		(
			SELECT COALESCE(array_to_json(array_agg(row_to_json(emp))), '[]') from (
						select id,nit,direccion,latitud,longitud,referencia,celular,fijo from usuario_tienda where id = tienda_id limit 1
					) emp
		) as empresa,
		(
			SELECT COALESCE(array_to_json(array_agg(row_to_json(items))), '[]') from (
				select i.descripcion as nombre,pi.cantidad as cantidad,pi.valor_unitario as valor from pedido_itemspedido as pi inner join pedido_items as i on(pi.pedido_id=id_pedido and pi.item_id=i.id)
			) items
		) as info,
		(
			select sum(pi.cantidad*pi.valor_unitario) from pedido_itemspedido as pi inner join pedido_items as i on(pi.pedido_id=id_pedido and pi.item_id=i.id)
		) as total
		from pedido_pedido where id = id_pedido limit 1
	) p);
end;
$$language plpgsql;
	select * from pedido_pedido
(SELECT COALESCE(array_to_json(array_agg(row_to_json(items))), '[]') from (
	select i.descripcion as nombre,pi.cantidad as cantidad,pi.valor_unitario as valor from pedido_itemspedido as pi inner join pedido_items as i on(pi.pedido_id=11 and pi.item_id=i.id)
) items

select i.descripcion as nombre,pi.cantidad as cantidad,pi.valor_unitario as valor from pedido_itemspedido as pi inner join pedido_items as i on(pi.pedido_id=11 and pi.item_id=i.id)

select * from pedido_itemspedido as pi inner join pedido_items as i on(pi.pedido_id=11 and pi.item_id=i.id)
select * from pedido_items
CREATE OR REPLACE FUNCTION ws_add_pedido_service(_json json)
  RETURNS text AS
$BODY$
declare
	x record;
	y record;
	tem json;
	t text;   			
	id_emp text;
	ot text;
	id_inser integer;
	error text:='';
	stop boolean :=true;
	val_item boolean;
	id_pedido integer;
	cont_pedido text:='';
	ban_pedido boolean :=true; 
	l json;
	ban_val_ind_emp boolean;
begin
		for x in select * from json_array_elements(_json::json->'pedido') loop 
			id_emp :=cast(x."value"::json->>'tienda' as json)->>'identificador'::text;
			select id::text from usuario_tienda where id = case when id_emp ~ '^[0-9]+$' then cast(id_emp as integer) else 0 end limit 1 into id_emp;
			if id_emp is not null then
				val_item:=true;
				<<uno>>
				for y in select nombre,case when cantidad~'^([0-9]+[.])?[0-9]+' then true else false end as cantidad,case when valor~'^([0-9]+[.])?[0-9]+' then true else false end as valor from json_populate_recordset(null::ws_descripcion,cast(x."value"::json->>'descripcion' as json)) loop
					if not y.cantidad or not y.valor then 
						val_item:=false;
						exit uno;
					end if;
				end loop;
				if val_item then
					insert into pedido_pedidows (detalle,num_pedido,npedido_express,cliente,fecha_pedido,tienda_id,tipo_pago,total,entregado,despachado,confirmado,alistado)
					values	(x."value",'','',x."value"::json->>'cliente',now(),cast(id_emp as integer),case when x."value"::json->>'tipo_pago'= '1' then 'Efectivo' when x."value"::json->>'tipo_pago' = '2' then 'Tarjeta' else 'Remision' end,cast(x."value"::json->>'total_pedido' as numeric),false,false,false,false)RETURNING id into id_inser;
					insert into pedido_timews(creado,pedido_id) values (now(),id_inser);
					SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
						select id,nit,direccion,latitud,longitud,referencia,celular,fijo from usuario_tienda where id = cast(id_emp as integer) limit 1
					) p into l;
					cont_pedido:=cont_pedido||case when not ban_pedido then ',' else''end||'{"id":'||id_inser||',"empresa":'||l||',"info":'||x."value"::json||'}';
					ban_pedido:=false;
				else
					error:=error||case when not stop then ',' else''end||x."value"::json;
				end if;
			else
				error:=error||case when not stop then ',' else''end||x."value"::json;
				stop:=false;
			end if;
			
		end loop;
		return '{"respuesta":true,"error":['||error||'],"pedidos":['||cont_pedido||']}';
	EXCEPTION WHEN others THEN
		return '{"respuesta":false,"mensage":"Error en la estructura del json"}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION ws_add_pedido_service(json)
  OWNER TO postgres;

select * from pedido_pedidows

{"pedido":[{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsd
ssds"},"tienda":{"identificador":"3"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000
}],"total_pedido":50000,"tipo_pago":1},{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dir
reccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"
jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}]}

{"pedido":[{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"3"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}]}


select * from json_array_elements('{"pedido":[{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"3"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}]}'::json->'pedido')
select * from json_each('{"pedido":[{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"3"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}]}')
