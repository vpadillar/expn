
CREATE OR REPLACE FUNCTION insertar_moto()
  RETURNS trigger AS
$BODY$
declare
begin
	IF (TG_OP = 'INSERT') THEN
		update motorizado_moto set estado=true where id = new.id;
	end if;
	return new;
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION insertar_moto()
  OWNER TO postgres;

CREATE TRIGGER insertar_moto
  AFTER INSERT
  ON motorizado_moto
  FOR EACH ROW
  EXECUTE PROCEDURE insertar_moto();