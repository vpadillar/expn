create or replace function get_add_pedido_admin(id_pedido integer) returns json as $$
declare 
begin
	return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select id, (select identifier from motorizado_motorizado where empleado_id=motorizado_id limit 1) as motorizado,10000*(select retraso from pedido_configuraciontiempo order by id desc limit 1) as retraso,
		(
			SELECT COALESCE(array_to_json(array_agg(row_to_json(emp))), '[]') from (
						select id,nit,direccion,latitud,longitud,referencia,celular,fijo from usuario_tienda where id = tienda_id limit 1
					) emp
		) as tienda,
		(
			SELECT COALESCE(array_to_json(array_agg(row_to_json(items))), '[]') from (
				select i.descripcion as nombre,pi.cantidad as cantidad,pi.valor_unitario as valor from pedido_itemspedido as pi inner join pedido_items as i on(pi.pedido_id=id_pedido and pi.item_id=i.id)
			) items
		) as info,
		(
			select sum(pi.cantidad*pi.valor_unitario) from pedido_itemspedido as pi inner join pedido_items as i on(pi.pedido_id=id_pedido and pi.item_id=i.id)
		) as total,
		(
			SELECT COALESCE(array_to_json(array_agg(row_to_json(emp_cli))), '[]') from (
						select first_name as nombre,last_name as apellidos,telefono_fijo as fijo,telefono_celular as celular,direccion from usuario_cliente where id = cliente_id
					) emp_cli
		) as cliente
		from pedido_pedido where id = id_pedido limit 1
	) p);
end;
$$language plpgsql;
