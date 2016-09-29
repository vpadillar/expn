-- Function: ws_add_pedido_service(json)

-- DROP FUNCTION ws_add_pedido_service(json);
select ws_add_pedido_service('{"pedido":{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},"pedido":{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}}')
select * from json_each('{"pedido":{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},"pedido":{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}}')

select cast("value"::json->>'tienda' as json)->>'identificadorer' from json_each('{"pedido":{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1},"pedido":{"id":"ws_ped","cliente":{"nombre":"mirlan","apellidos":"Reyes Polo","identificacion":"45454545454","dirreccion":"dsdsdsdsddsdsdsdsdssds"},"tienda":{"identificador":"123456"},"descripcion":[{"nombre":"jajaja","cantidad":5,"valor":1000},{"nombre":"jajaja","cantidad":5,"valor":1000}],"total_pedido":50000,"tipo_pago":1}}')

select "value"::json->>'valor' ~ '^([0-9]+[.])?[0-9]+',"value"::json->>'valor' from json_each('{"pedido":{"valor":"155452"},"pedido":{"valor":"dsdssdsdsds"}}')

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
begin
		for x in select * from json_each(_json) loop
			id_emp :=cast(x."value"::json->>'tienda' as json)->>'identificador'::text;
			select id::text from usuario_empresa where nit like ''||case when id_emp is not null then id_emp::text else '0' end||'' limit 1 into id_emp;
			raise notice 'tupla  %',x."value"::json;
			raise notice 'el valor del id de empresa es %',id_emp;
			if id_emp is not null then
				for y in select * from json_populate_recordset(null::ws_descripcion,cast(x."value"::json->>'descripcion' as json)) loop
					raise notice '% % %',y.nombre,y.cantidad,y.valor;
				end loop;
				insert into pedido_pedidows
					(num_pedido,npedido_express,cliente,empresa_id,fecha_pedido,tienda,tipo_pago,total,entregado,despachado,confirmado,alistado)
				values	('','',x."value"::json->>'cliente',cast(id_emp as integer),now(),cast(x."value"::json->>'tienda' as json)->>'tienda'::text,case when x."value"::json->>'tipo_pago'= '1' then 'Efectivo' when x."value"::json->>'tipo_pago' = '2' then 'Tarjeta' else 'Remision' end,cast(x."value"::json->>'total_pedido' as numeric),false,false,false,false)RETURNING id into id_inser;
				insert into pedido_timews(creado,pedido_id) values (now(),id_inser);
			else
				error:=error||case when not stop then ',' else''end||x."value"::json;
				raise notice 'El acumulado del error % ',error;
				stop:=false;
			end if;
		end loop;
	return '{"respuesta":true}';
EXCEPTION WHEN others THEN
	raise notice 'descripcion';
	return '{"respuesta":false,"mensage":"Error en la estructura del json"}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION ws_add_pedido_service(json)
  OWNER TO postgres;


--select * from pedido_pedido
--select * from usuario_empresa
--update pedido_pedido set total= case when id%2=0 then 2222.365 else 595959 end