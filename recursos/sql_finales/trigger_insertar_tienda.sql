-- Function: crear_token()

-- DROP FUNCTION crear_token();

CREATE OR REPLACE FUNCTION crear_token()
  RETURNS trigger AS
$BODY$
declare
begin
	update usuario_tienda set token= md5(case when new.nombre is not null and length(new.nombre) > 0 then new.nombre else cast(old.id as text) end) where id=new.id;
	return new;
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION crear_token()
  OWNER TO postgres;

CREATE TRIGGER crear_token
  AFTER INSERT
  ON usuario_tienda
  FOR EACH ROW
  EXECUTE PROCEDURE crear_token();
