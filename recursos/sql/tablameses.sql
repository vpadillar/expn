-- Function: tablameses(date)

-- DROP FUNCTION tablameses(date);

CREATE OR REPLACE FUNCTION tablameses(f date)
  RETURNS text AS
$BODY$
declare
	a text[] :='{" de Enero de "," de Febrero de "," de Marzo de "," de Abril de "," de Mayo de "," de 
Junio de "," de Julio de "," de Agosto de "," de Septiembre de "," de Octubre de "," de Noviembre de "," de Diciembre de "}';
begin
	return (extract(day from f)||a[extract(month from f)]||extract(year from f));
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION tablameses(date)
  OWNER TO postgres;
