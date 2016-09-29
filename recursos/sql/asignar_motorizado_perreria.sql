
create or replace function asignar_motorizado_perr(id_pedido integer, id_moto text) returns text as $$
declare
   motorizado integer;
   r integer;
begin	
	select * from usuario_empleado where cargo=('MOTORIZADO') and usuario_ptr_id = (select user_ptr_id from usuario_usuario where identificacion='12345678' limit 1) limit 1 into motorizado;
	if motorizado is not null then 
		select * from pedido_pedido where id=id_pedido and motorizado_id is null limit 1 into r;
		if r is not null then
			update pedido_pedido set motorizado_id = motorizado where id=id_pedido;
			return 'True';
		end if;
	end if;
	return 'False';
end;
$$language plpgsql;

