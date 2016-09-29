create or replace function comfiguracion_tiempos_empresa() returns trigger as $$
declare 
begin 
	insert into pedido_configuraciontiempo (retraso,pedido,distancia,empresa_id,primero,segundo,gps) values(3,3,1000,new.id,1,15,1);
	return new;
end;
$$language plpgsql;

create trigger comfiguracion_tiempos_empresa after insert on usuario_empresa
	for each row execute procedure comfiguracion_tiempos_empresa()


