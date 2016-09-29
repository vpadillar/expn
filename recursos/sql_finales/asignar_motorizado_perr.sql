-- Function: asignar_motorizado_perr(integer, integer)

-- DROP FUNCTION asignar_motorizado_perr(integer, integer);

CREATE OR REPLACE FUNCTION asignar_motorizado_perr(id_pedido integer, id_moto integer)
  RETURNS text AS
$BODY$
declare
   r integer;
begin
	select * from usuario_empleado where cargo=('MOTORIZADO') and usuario_ptr_id=8 limit 1 into r;
	if r is not null then
		select * from pedido_pedido where id=id_pedido and motorizado_id is null limit 1 into r;
		if r is not null then
			update pedido_pedido set motorizado_id = id_moto where id=id_pedido;
			return 'True';
		end if;
	end if;
	return 'False';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION asignar_motorizado_perr(integer, integer)
  OWNER TO postgres;
