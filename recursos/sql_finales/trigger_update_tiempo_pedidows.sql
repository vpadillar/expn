-- Function: update_tiempo_pedidows()

-- DROP FUNCTION update_tiempo_pedidows();

CREATE OR REPLACE FUNCTION update_tiempo_pedidows()
  RETURNS trigger AS
$BODY$
declare
begin
	if new.despachado and old.despachado = false then
		update pedido_timews set despachado = now() where pedido_id= old.id;
	elsif new.entregado and old.entregado=false then
		update pedido_timews set entregado = now() where pedido_id= old.id;
	elsif new.confirmado and old.confirmado=false then
		update pedido_timews set confirmado = now() where pedido_id= old.id;
	end if;
	return new;
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION update_tiempo_pedidows()
  OWNER TO postgres;


create trigger update_tiempo_pedidows after update on pedido_pedidows
	for each row execute procedure update_tiempo_pedidows()
