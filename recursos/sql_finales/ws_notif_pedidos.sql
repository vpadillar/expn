-- Function: ws_notif_pedidos(integer)

-- DROP FUNCTION ws_notif_pedidos(integer);

CREATE OR REPLACE FUNCTION ws_notif_pedidos(id_user integer)
  RETURNS json AS
$BODY$
 declare
	id_nit_tien integer;
 begin
	/*select nit from domicilios_empresa where id = (select empresa_id from domicilios_empleado where usuario_ptr_id=id_user limit 1) limit 1 into id_nit_tien;*/
	select empresa_id from domicilios_empleado where usuario_ptr_id=id_user limit 1 into id_nit_tien;
	if id_nit_tien is null then
		id_nit_tien:=0;
	end if;
	return (
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select id,cast(cliente as json)->>'nombre'::text as nom,
			       cast(cliente as json)->>'apellidos'::text as apellido,
			       cast(cliente as json)->>'dirreccion'::text as dir,
			       (
					select t.nombre from domicilios_tienda as t where t.nit = tienda limit 1
			       ) as emp,
			       (
					select t.direccion from domicilios_tienda as t where t.nit = tienda limit 1
			       ) as emp_dir
			       from domicilios_pedidows where empresa_id=id_nit_tien
		) p
	);
 end;
 $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION ws_notif_pedidos(integer)
  OWNER TO postgres;
