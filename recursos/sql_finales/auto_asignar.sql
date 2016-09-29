-- Function: auto_asignar(integer, json)

-- DROP FUNCTION auto_asignar(integer, json);

CREATE OR REPLACE FUNCTION auto_asignar(tienda_pk integer, motorizado_json json)
  RETURNS text AS
$BODY$
declare
	d numeric;
	result text;
begin
	d := (select last(distancia) from public.pedido_configuraciontiempo);
	result := (select
		motorizado.identifier
	from public.motorizado_motorizado as motorizado
	left join public.pedidos_motorizados as pedido on motorizado.empleado_id = pedido.motorizado_id
	join (select nombre, (latitud ||','|| longitud), (lat ||','|| lng), (degrees(ST_Distance(ST_GeomFromText('POINT('|| ti.latitud ||' '|| ti.longitud ||')'), ST_GeomFromText('POINT('|| n.lat ||' '|| n.lng ||')'))) * 2000), identificador from usuario_tienda as ti
		join (select * from json_populate_recordset(null::t, motorizado_json)) as n
			on (degrees(ST_Distance(ST_GeomFromText('POINT('|| ti.latitud ||' '|| ti.longitud ||')'), ST_GeomFromText('POINT('|| n.lat ||' '|| n.lng ||')'))) * 2000) < d
		where id=tienda_pk) as distance on distance.identificador = motorizado.identifier
	group by motorizado.id
	order by last(pedido.creado) desc nulls first limit 1)::text;
	if result is null then
		return (select
			motorizado.identifier
		from public.motorizado_motorizado as motorizado
		join public.usuario_empleado as empleado on motorizado.empleado_id = empleado.usuario_ptr_id
		join public.usuario_tienda as tienda on tienda.id= empleado.tienda_id and tienda.id = tienda_pk and empleado.ciudad_id = tienda.ciudad_id
		join (select * from json_populate_recordset(null::t, motorizado_json)) as n
			on motorizado.identifier = n.identificador
		order by (degrees(ST_Distance(ST_GeomFromText('POINT('|| tienda.latitud ||' '|| tienda.longitud ||')'), ST_GeomFromText('POINT('|| n.lat ||' '|| n.lng ||')'))) * 2000) asc
		limit 1)::text;
	end if;
	return result;
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION auto_asignar(integer, json)
  OWNER TO postgres;
