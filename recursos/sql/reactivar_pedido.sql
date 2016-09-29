select reactivar_pedido(10)
create or replace function reactivar_pedido(id_ped integer) returns json as $$
declare 
	pedido record;
	id_pedido integer;
	nom_pedido text;
	v_nom text[];
	motorizado_identifier text;
begin
	select * from pedido_pedido where id = id_ped limit 1 into pedido;
	select num_pedido from pedido_pedido as p  order by p.id desc limit 1 into nom_pedido;
	if pedido.id is not null then
		select identifier from motorizado_motorizado where empleado_id = pedido.motorizado_id limit 1 into motorizado_identifier;
		if motorizado_identifier is not null then
			select string_to_array(nom_pedido, '_') into v_nom;
			nom_pedido:=v_nom[1]||'_'||cast(v_nom[2] as numeric)+1;
			insert into pedido_pedido
			   (num_pedido,npedido_express,fecha_pedido,tipo_pago,total,entregado,despachado,confirmado,alistado,alistador_id,cliente_id,empresa_id,motorizado_id,supervisor_id,tienda_id,notificado,activado,reactivacion)
			   values 
			   (nom_pedido,nom_pedido,now(),pedido.tipo_pago,pedido.total,false,false,false,false,pedido.alistador_id,pedido.cliente_id,pedido.empresa_id,pedido.motorizado_id,pedido.supervisor_id,pedido.tienda_id,false,true,false) returning id into id_pedido;
			   insert into pedido_itemspedido (cantidad,valor_unitario,valor_total,item_id,pedido_id) select cantidad,valor_unitario,valor_total,item_id,id_pedido from pedido_itemspedido where pedido_id=id_ped;
			   
			   return (array_to_json(array_agg(row_to_json(row(id_pedido,motorizado_identifier,get_add_pedido_admin(id_pedido))))));
		end if;
	end if;
	return get_add_pedido_admin(id_pedido);
	
end;
$$language plpgsql;
drop function reactivar_pedido(int)

--select last(id) from pedido_pedido
--select num_pedido from pedido_pedido as p  order by p.id desc limit 1
--select string_to_array('EX_12', '_')

--select * from pedido_itemspedido wher pedido_id