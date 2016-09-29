-- Function: get_info_empleados_report_act(integer, text, text, boolean)

-- DROP FUNCTION get_info_empleados_report_act(integer, text, text, boolean);

CREATE OR REPLACE FUNCTION get_info_empleados_report_act(id_emp integer, fecha1 text, fecha2 text, state boolean)
  RETURNS json AS
$BODY$
declare
	emp json;
	dat json;
begin
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select u.identificacion as iden,a.first_name||' '||a.last_name as nom,e.direccion as dir,
			'Tel : '||u.telefono_fijo||'-'||u.telefono_celular as tel,a.email as correo
			from usuario_empleado as e
			inner join usuario_usuario as u on (e.usuario_ptr_id=u.user_ptr_id)
			inner join auth_user as a on(a.id=u.user_ptr_id and a.id=id_emp) limit 1
	) p into emp;
	SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select cliente,total,direccion,motori,alistar,despacho,entrega
			from pedidos_tiempos_actualizada where fecha BETWEEN fecha1::date AND fecha2::date and estado = state
				and (supervisor_id=id_emp or alistador_id=id_emp or motorizado_id=id_emp)
	) p into dat;
	return (array_to_json(array_agg(row_to_json(row(emp,dat)))));
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION get_info_empleados_report_act(integer, text, text, boolean)
  OWNER TO postgres;
