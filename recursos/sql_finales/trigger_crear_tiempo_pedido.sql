-- Function: crear_tiempo_pedido()

-- DROP FUNCTION crear_tiempo_pedido();

CREATE OR REPLACE FUNCTION crear_tiempo_pedido()
  RETURNS trigger AS
$BODY$
declare
begin
	insert into pedido_time(pedido_id,creado) values (new.id,now());
	return new;
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION crear_tiempo_pedido()
  OWNER TO postgres;


CREATE TRIGGER crear_tiempo_pedido
  AFTER INSERT
  ON pedido_pedido
  FOR EACH ROW
  EXECUTE PROCEDURE crear_tiempo_pedido();
