-- Function: aceptar_pw_service(integer, text)

-- DROP FUNCTION aceptar_pw_service(integer, text);

CREATE OR REPLACE FUNCTION aceptar_pw_service(id_pedido integer, idt_motor text)
  RETURNS text AS
$BODY$
declare
	pedido record;
	motorizado record;
begin
	select * from pedido_pedidows as pw inner join usuario_tienda as t on(pw.tienda_id=t.id and pw.id= id_pedido) limit 1 into pedido;
	if pedido.id is not null then
		select * from motorizado_motorizado as m inner join usuario_empleado as e on (m.empleado_id=e.usuario_ptr_id and m.identifier=idt_motor and e.empresa_id=1)  limit 1 into motorizado;
		if motorizado.id is not null then
			update pedido_pedidows set motorizado_id = motorizado.usuario_ptr_id, confirmado=true where id = id_pedido;
			return '{"r":true}';
		end if;
	end if;
	return '{"r":false}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION aceptar_pw_service(integer, text)
  OWNER TO postgres;
