-- Function: eliminar_moto()

-- DROP FUNCTION eliminar_moto();

CREATE OR REPLACE FUNCTION eliminar_moto()
  RETURNS trigger AS
$BODY$
declare
begin
	IF (TG_OP = 'DELETE') THEN
		update motorizado_moto set estado=false where id = old.id;
	end if;
	return null;
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION eliminar_moto()
  OWNER TO postgres;

CREATE TRIGGER eliminar_moto
  BEFORE DELETE
  ON motorizado_moto
  FOR EACH ROW
  EXECUTE PROCEDURE eliminar_moto();
